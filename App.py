import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import csv
import os
import pandas as pd


file_name = "running_data.csv"



st.set_page_config(
    page_title="Running Log",
    page_icon="🏃",
    layout="centered"
)



def time_to_seconds(time_text):

    hour, minute, second = map(
        int,
        time_text.split(":")
    )

    return hour * 3600 + minute * 60 + second



def seconds_to_time(total_seconds):

    total_seconds = int(total_seconds)

    hour = total_seconds // 3600
    minute = (total_seconds % 3600) // 60
    second = total_seconds % 60

    return f"{hour:02d}:{minute:02d}:{second:02d}"


# แปลงจำนวนวินาทีให้อ่านง่าย
def seconds_to_text(total_seconds):

    total_seconds = abs(int(total_seconds))

    hour = total_seconds // 3600
    minute = (total_seconds % 3600) // 60
    second = total_seconds % 60

    if hour > 0:

        return (
            f"{hour} ชั่วโมง "
            f"{minute} นาที "
            f"{second} วินาที"
        )

    elif minute > 0:

        return (
            f"{minute} นาที "
            f"{second} วินาที"
        )

    else:

        return f"{second} วินาที"


# =========================
# อ่านข้อมูลไว้ก่อน
# =========================

data = None

if os.path.exists(file_name):

    data = pd.read_csv(file_name)

    if data.empty:
        data = None


# =========================
# หัวเว็บ + เมนูมุมขวาบน
# =========================

title_col, menu_col = st.columns([3, 1])


with title_col:

    st.title("🏃 Running Log")

    st.caption(
        "บันทึกและติดตามพัฒนาการการวิ่ง"
    )


with menu_col:

    with st.popover(
        "🏃 ระยะเวลาการวิ่ง"
    ):

        if data is not None:

            date_data = data.copy()

            # แปลงวันที่จาก CSV เป็นวันที่จริง
            date_data["Date"] = pd.to_datetime(
                date_data["Date"],
                errors="coerce"
            )

            valid_dates = (
                date_data["Date"]
                .dropna()
            )

            if not valid_dates.empty:

                today = date.today()

                # วันที่เริ่มวิ่ง
                first_run = (
                    valid_dates
                    .min()
                    .date()
                )

                # วันที่วิ่งล่าสุด
                last_run = (
                    valid_dates
                    .max()
                    .date()
                )

                # จำนวนวันที่ออกวิ่งจริง
                running_days = (
                    valid_dates
                    .dt.date
                    .nunique()
                )

                # ระยะเวลาตั้งแต่เริ่มจนถึงวันนี้
                running_period = relativedelta(
                    today,
                    first_run
                )

                # ขาดช่วงจากครั้งล่าสุดกี่วัน
                break_days = max(
                    0,
                    (today - last_run).days
                )


                st.write(
                    "### 🏁 การวิ่งของคุณ"
                )

                st.write(
                    "เริ่มวิ่งครั้งแรก:",
                    first_run.strftime(
                        "%d/%m/%Y"
                    )
                )

                st.write(
                    "วิ่งล่าสุด:",
                    last_run.strftime(
                        "%d/%m/%Y"
                    )
                )

                st.write(
                    "วันที่ออกวิ่งจริง:",
                    f"{running_days} วัน"
                )


                # =========================
                # ระยะเวลาที่เริ่มวิ่งมา
                # =========================

                period_parts = []

                if running_period.years > 0:

                    period_parts.append(
                        f"{running_period.years} ปี"
                    )

                if running_period.months > 0:

                    period_parts.append(
                        f"{running_period.months} เดือน"
                    )

                if running_period.days > 0:

                    period_parts.append(
                        f"{running_period.days} วัน"
                    )


                if period_parts:

                    period_text = " ".join(
                        period_parts
                    )

                else:

                    period_text = "เริ่มวันนี้"


                st.info(
                    f"วิ่งมาแล้ว {period_text}"
                )


                # =========================
                # ขาดช่วง
                # =========================

                if break_days == 0:

                    st.success(
                        "วันนี้มีบันทึกการวิ่งแล้ว 🏃"
                    )

                elif break_days == 1:

                    st.info(
                        "วิ่งล่าสุดเมื่อวาน"
                    )

                else:

                    st.warning(
                        f"ไม่ได้บันทึกการวิ่งมา "
                        f"{break_days} วันแล้ว"
                    )


                # =========================
                # Milestone
                # =========================

                one_month_date = (
                    first_run
                    + relativedelta(months=1)
                )

                one_year_date = (
                    first_run
                    + relativedelta(years=1)
                )


                if today >= one_year_date:

                    st.success(
                        f"🎉 เริ่มวิ่งมาแล้ว "
                        f"{running_period.years} ปี"
                    )


                elif today >= one_month_date:

                    st.success(
                        "🎉 เริ่มวิ่งครบ 1 เดือนแล้ว"
                    )

                    days_until_year = (
                        one_year_date - today
                    ).days

                    st.caption(
                        f"อีก {days_until_year} วัน "
                        f"จะครบ 1 ปี"
                    )


                else:

                    days_until_month = (
                        one_month_date - today
                    ).days

                    st.caption(
                        f"อีก {days_until_month} วัน "
                        f"จะครบ 1 เดือน"
                    )


            else:

                st.info(
                    "ยังไม่มีข้อมูลวันที่ที่ถูกต้อง"
                )


        else:

            st.info(
                "ยังไม่มีข้อมูลการวิ่ง"
            )


# =========================
# ส่วนบันทึกข้อมูล
# =========================

run_date = st.date_input(
    "วันที่วิ่ง",
    value=date.today()
)


distance = st.number_input(
    "ระยะทางที่วิ่ง (km)",
    min_value=0.0,
    step=0.1
)


st.write("เวลาที่ใช้")


time_col1, time_col2, time_col3 = (
    st.columns(3)
)


with time_col1:

    hour = st.number_input(
        "ชั่วโมง",
        min_value=0,
        step=1
    )


with time_col2:

    minute = st.number_input(
        "นาที",
        min_value=0,
        max_value=59,
        step=1
    )


with time_col3:

    second = st.number_input(
        "วินาที",
        min_value=0,
        max_value=59,
        step=1
    )


# =========================
# ปุ่มบันทึก
# =========================

if st.button(
    "บันทึกการวิ่ง",
    use_container_width=True
):

    total_seconds = (
        hour * 3600
        + minute * 60
        + second
    )


    if distance > 0 and total_seconds > 0:

        pace_seconds = (
            total_seconds / distance
        )

        pace_minute = int(
            pace_seconds // 60
        )

        pace_second = int(
            pace_seconds % 60
        )


        run_time = (
            f"{hour:02d}:"
            f"{minute:02d}:"
            f"{second:02d}"
        )


        pace = (
            f"{pace_minute}:"
            f"{pace_second:02d}"
        )


        file_exists = os.path.exists(
            file_name
        )


        with open(
            file_name,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)


            if not file_exists:

                writer.writerow([
                    "Date",
                    "Distance_km",
                    "Time",
                    "Pace"
                ])


            writer.writerow([
                run_date,
                distance,
                run_time,
                pace
            ])


        st.success(
            "บันทึกการวิ่งเรียบร้อย!"
        )

        st.write(
            "วันที่:",
            run_date
        )

        st.write(
            "ระยะทาง:",
            distance,
            "km"
        )

        st.write(
            "เวลา:",
            run_time
        )

        st.write(
            "Pace:",
            pace,
            "min/km"
        )


        # โหลดหน้าใหม่เพื่อให้สถิติล่าสุดทันที
        st.rerun()


    else:

        st.warning(
            "กรุณากรอกระยะทางและเวลา"
        )


# =========================
# โหลดข้อมูลใหม่
# =========================

if os.path.exists(file_name):

    data = pd.read_csv(file_name)

else:

    data = None


# =========================
# แสดงข้อมูล
# =========================

if data is not None and not data.empty:

    # =========================
    # สรุปการวิ่งทั้งหมด
    # =========================

    st.subheader(
        "📊 สรุปการวิ่งทั้งหมด"
    )


    total_distance = (
        data["Distance_km"].sum()
    )


    total_runs = len(data)


    total_time_seconds = (
        data["Time"]
        .apply(time_to_seconds)
        .sum()
    )


    average_pace_seconds = round(
        total_time_seconds
        / total_distance
    )


    average_pace_minute = (
        average_pace_seconds // 60
    )


    average_pace_second = (
        average_pace_seconds % 60
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "ระยะทางรวม",
            f"{total_distance:.2f} km"
        )


    with col2:

        st.metric(
            "จำนวนครั้ง",
            f"{total_runs} ครั้ง"
        )


    with col3:

        st.metric(
            "เวลารวม",
            seconds_to_text(
                total_time_seconds
            )
        )


    with col4:

        st.metric(
            "Pace เฉลี่ย",
            f"{average_pace_minute}:"
            f"{average_pace_second:02d} min/km"
        )


    # =========================
    # ประวัติการวิ่ง
    # =========================

    with st.expander(
        "📋 ดูประวัติการวิ่ง"
    ):

        # สร้างสำเนาข้อมูลสำหรับแสดงผล
        display_data = data.copy()

        # เพิ่มคอลัมน์ "ครั้งที่"
        # โดยเริ่มจาก 1
        display_data.insert(
            0,
            "ครั้งที่",
            range(
                1,
                len(display_data) + 1
            )
        )

        # ซ่อน Index เดิมของ Pandas
        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )


    # =========================
    # สถิติแต่ละระยะ
    # =========================

    with st.expander(
        "📊 ดูสถิติแต่ละระยะ"
    ):

        distance_list = (
            data["Distance_km"]
            .unique()
        )


        selected_distance = (
            st.selectbox(
                "เลือกระยะทาง",
                distance_list
            )
        )


        selected_data = data[
            data["Distance_km"]
            == selected_distance
        ].copy()


        selected_data[
            "Time_seconds"
        ] = (
            selected_data["Time"]
            .apply(time_to_seconds)
        )


        st.write(
            "ระยะที่เลือก:",
            selected_distance,
            "km"
        )


        latest_time = (
            selected_data
            .iloc[-1]["Time_seconds"]
        )


        best_time = (
            selected_data[
                "Time_seconds"
            ]
            .min()
        )


        st.write(
            "เวลาล่าสุด:",
            seconds_to_time(
                latest_time
            )
        )


        st.write(
            "เวลาที่ดีที่สุด:",
            seconds_to_time(
                best_time
            )
        )


        # =========================
        # เปรียบเทียบครั้งก่อน
        # =========================

        if len(selected_data) >= 2:

            previous_time = (
                selected_data
                .iloc[-2][
                    "Time_seconds"
                ]
            )


            difference = (
                latest_time
                - previous_time
            )


            percentage = (
                abs(difference)
                / previous_time
                * 100
            )


            difference_text = (
                seconds_to_text(
                    difference
                )
            )


            st.write(
                "ครั้งก่อน:",
                seconds_to_time(
                    previous_time
                )
            )


            if difference < 0:

                st.success(
                    f"เร็วขึ้น "
                    f"{difference_text} "
                    f"({percentage:.2f}%) 🎉"
                )


            elif difference > 0:

                st.warning(
                    f"ช้าลง "
                    f"{difference_text} "
                    f"({percentage:.2f}%)"
                )


            else:

                st.info(
                    "เวลาเท่ากับครั้งก่อน"
                )


        else:

            st.info(
                "ยังมีข้อมูลระยะนี้เพียง "
                "1 ครั้ง จึงยังเปรียบเทียบไม่ได้"
            )


else:

    st.info(
        "ยังไม่มีข้อมูลการวิ่ง"
    )


# =========================
# จัดการข้อมูล
# =========================

with st.expander(
    "⚙️ จัดการข้อมูล"
):

    confirm_reset = st.checkbox(
        "ฉันต้องการลบประวัติการวิ่งทั้งหมด"
    )


    if st.button(
        "🗑️ รีเซ็ตข้อมูล"
    ):

        if confirm_reset:

            if os.path.exists(
                file_name
            ):

                os.remove(
                    file_name
                )

                st.success(
                    "ลบข้อมูลการวิ่งทั้งหมดเรียบร้อยแล้ว"
                )

                st.rerun()


            else:

                st.info(
                    "ยังไม่มีข้อมูลให้ลบ"
                )


        else:

            st.warning(
                "กรุณาติ๊กยืนยันก่อนรีเซ็ตข้อมูล"
            )