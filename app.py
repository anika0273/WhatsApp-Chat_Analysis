import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns


st.sidebar.title("WhatsApp Chat Analysis")
upload_file = st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users

    user_list = df['User'].unique().tolist()
    user_list = list(set(user_list))
    user_list.remove('MIT Data Science')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis w.r.t ", user_list)

    grp_participant = len(user_list)
    st.sidebar.write("Number of Participant:", grp_participant)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, image, links = helper.fetch(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Images")
            st.title(image)
        with col4:
            st.header("Total Links")
            st.title(links)


        #montly timeline
        timeline = helper.monthly_timeline(selected_user,df)
        st.header("Monthly Chat Analysis")
        plt.plot(timeline['Time'], timeline['Message'])
        plt.xticks(rotation=45)
        st.pyplot()

        #daily timeline
        timeline_daily = helper.daily_timeline(selected_user, df)
        st.header("Daily Chat Analysis")
        plt.plot(timeline_daily['Only_Date'], timeline_daily['Message'])
        plt.xticks(rotation=45)
        st.pyplot()

        #Activity map
        timeline_week_day = helper.wk_day(selected_user, df)
        st.header("WeekDay and Monthly Chat Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Weekday Statistics")
            st.dataframe(timeline_week_day)
            st.header("Most Active day of the Week")
            st.bar_chart(timeline_week_day, x="DayOfTheWeek", y="Message")
            plt.plot(timeline_week_day['DayOfTheWeek'], timeline_week_day['Message'])
            plt.xticks(rotation=45)
            st.pyplot()
        with col2:
            st.header("Monthly Statistics")
            mnth = helper.monthly_activity(selected_user,df)
            st.dataframe(mnth)
            st.header("Most Active Month [Sept-January]")
            st.bar_chart(mnth, x="Month", y="Count")
            plt.plot(mnth['Month'], mnth['Count'])
            plt.xticks(rotation=45)
            st.pyplot()

        #heatmap
        st.header("A HeatMap Representation of WeekDay and Time of the Day Analysis")
        activity_map = helper.heat_plot(selected_user,df)
        sns.heatmap(activity_map, annot=True, cmap='hot')
        st.pyplot()

        #find the busiest user
        if selected_user == "Overall":
            st.title("Most Busy user")
            x, prcnt_df = helper.fetch_most_busy(df)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.bar_chart(x)
            with col2:
                st.dataframe(prcnt_df)
            with col3:
                st.bar_chart(prcnt_df.head(10))

        #wordcloud
        st.title("WordCloud")
        wordcloud = helper.create_wordcloud(selected_user, df)
        st.image(Image.fromarray(wordcloud.to_array()), use_column_width=True)

        #most common words
        st.title("Most Common Words")
        most_common_words = helper.most_common_words(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_words)
        with col2:
            st.bar_chart(most_common_words.iloc[5:25], x="Words", y="Frequency")


        # Most Used Emojis
        st.title("Most Used Emojis")
        emojis = helper.emoji_helper(selected_user,df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.dataframe(emojis)
        with col2:
            st.bar_chart(emojis.iloc[:10], x="Emoji", y="Frequency")
        with col3:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.write(emojis.iloc[:5].plot.pie(y='Frequency', labels=emojis['Emoji'], autopct='%1.1f%%'))
            st.pyplot()


