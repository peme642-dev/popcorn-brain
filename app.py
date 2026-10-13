import streamlit as st
from google import genai
import time
import re

st.set_page_config(
    page_title="Popcorn Brain | Chuyên gia AI tư vấn",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #FBF9F1; 
        color: #1B365D; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    h1, h2, h3, h4 {
        color: #1B365D !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .nguyen-nhan-title {
        color: #1B365D !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 1.75rem;
        margin-bottom: 1rem;
    }
    .stMainBlockContainer div[data-testid="stExpander"] {
        background-color: #F5D6E0 !important; 
        border: 1px solid #E6B8C7 !important;
        border-radius: 4px !important;
        margin-bottom: 8px !important;
    }
    .stMainBlockContainer div[data-testid="stExpander"] summary {
        color: #1B365D !important; 
        font-weight: 700 !important; 
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 10px 14px !important;
    }
    .stMainBlockContainer div[data-testid="stExpander"][aria-expanded="true"] {
        background-color: #F0C4D3 !important;
    }
    .stMainBlockContainer div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background-color: #F0C4D3 !important; 
        color: #000000 !important;          
        border-top: 1px solid #E6B8C7 !important;
        padding: 14px !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }
    .expert-card {
        background-color: #F5D6E0;
        padding: 24px;
        border-radius: 6px;
        margin-top: 20px;
        margin-bottom: 25px;
        border-left: 6px solid #1B365D;
        border-top: 1px solid #E6B8C7;
        border-right: 1px solid #E6B8C7;
        border-bottom: 1px solid #E6B8C7;
        text-align: center;
    }
    .expert-card p {
        color: #1B365D !important;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.6;
    }
    .intro-text {
        font-size: 1.05rem;
        line-height: 1.7;
        margin-bottom: 18px;
        text-align: justify;
        color: #1B365D;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F5D6E0 !important;
        color: #1B365D !important;
        border-radius: 6px 6px 0 0;
        font-weight: 700;
        padding: 12px 24px;
        border: 1px solid #E6B8C7;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F5D6E0 !important;
        color: #000000 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #000000 !important;
    }
    /* ĐỔI CHỮ Ô NHẬP TIN NHẮN VÀ CÂU TRẢ LỜI CỦA AI THÀNH MÀU ĐEN */
    .stChatInput textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    .stChatInput textarea::placeholder {
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
    }
    [data-testid="stChatMessage"] {
        color: #000000 !important;
    }
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] li, 
    [data-testid="stChatMessage"] span {
        color: #000000 !important;
    }

    /* HIỆU ỨNG KHỐI CHỮ ĐEN NGHIÊNG TRƯỢT RA */
    @keyframes slideInFromLeft {
        0% {
            transform: skew(-15deg) translateX(-150px);
            opacity: 0;
        }
        100% {
            transform: skew(-15deg) translateX(0);
            opacity: 1;
        }
    }
    .scroll-reveal-container {
        width: 100%;
        overflow: hidden;
        padding: 20px 0;
        background: transparent;
        margin-bottom: 15px;
    }
    .scroll-reveal-box {
        display: inline-block;
        background-color: #1A1A1A;
        color: #FFFFFF;
        padding: 12px 28px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 3rem;
        font-weight: 900;
        text-transform: uppercase;
        box-shadow: 4px 4px 0px #E6B8C7;
        letter-spacing: 2px;
        animation: slideInFromLeft 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    </style>
""", unsafe_allow_html=True)

# CẤU HÌNH API KEY
API_KEY = st.secrets.get("GEMINI_API_KEY", "").strip()

if not API_KEY:
    st.error("Chưa cấu hình GEMINI_API_KEY trong Streamlit Secrets.")
    st.stop()

client = genai.Client(
    api_key=API_KEY,
    vertexai=False
)

# BANNER POPCORN BRAIN HIỆU ỨNG NỀN ĐEN NGHIÊNG
st.markdown("""
    <div class="scroll-reveal-container">
        <div class="scroll-reveal-box">
            POPCORN BRAIN 🍿🔥✨
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
tab1, tab2 = st.tabs(["📌 NỘI DUNG NGHIÊN CỨU", "💬 TƯ VẤN CÙNG CHUYÊN GIA AI"])

with tab1:
    st.markdown("""
    <div class="intro-text">
    Thuật ngữ <b>"Popcorn Brain"</b> được nhà nghiên cứu David M. Levy (Đại học Washington, Hoa Kỳ) đưa ra lần đầu vào năm 2011, sử dụng để mô tả trạng thái con người trở nên quen thuộc với việc tiếp nhận các kích thích số nhanh, liên tục và đa dạng đến mức khó duy trì sự chú ý đối với những hoạt động có nhịp độ chậm hơn, đòi hỏi sự tập trung và suy nghĩ sâu.
    </div>
    <div class="intro-text">
    Cần nhấn mạnh rằng, hiện nay "hội chứng não bỏng ngô" chưa được công nhận là một bệnh lý hay một rối loạn tâm thần chính thức trong các hệ thống phân loại bệnh quốc tế. Thuật ngữ này chủ yếu được sử dụng để mô tả một nhóm biểu hiện về nhận thức và hành vi có thể xuất hiện khi con người thường xuyên tiếp xúc với các kích thích số có cường độ cao và thay đổi liên tục.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="nguyen-nhan-title">NGUYÊN NHÂN HÌNH THÀNH</div>', unsafe_allow_html=True)
        with st.expander("TẦN SUẤT TIẾP XÚC VỚI CÁC KÍCH THÍCH SỐ NHANH VÀ LIÊN TỤC"):
            st.write("Việc thường xuyên tiếp xúc với video ngắn, nội dung được cập nhật liên tục và các thông báo tức thời có thể làm gia tăng xu hướng tìm kiếm sự mới lạ và phản hồi nhanh.")
        with st.expander("THÓI QUEN SỬ DỤNG ĐIỆN THOẠI CHO MỤC ĐÍCH GIẢI TRÍ"):
            st.write("Việc sử dụng điện thoại trong thời gian dài, đặc biệt là các hoạt động giải trí có tính kích thích cao, có thể liên quan đến khả năng duy trì sự chú ý và tự điều chỉnh hành vi.")
        with st.expander("KHẢ NĂNG TỰ ĐIỀU CHỈNH HÀNH VI"):
            st.write("Những học sinh có kỹ năng tự nhận thức, tự giám sát và tự kiểm soát hành vi tốt hơn có thể thích ứng hiệu quả hơn với môi trường số và giảm nguy cơ xuất hiện các biểu hiện của 'hội chứng não bỏng ngô'.")
        with st.expander("MỨC ĐỘ THAM GIA CÁC HOẠT ĐỘNG NGOÀI MÔI TRƯỜNG SỐ"):
            st.write("Việc tham gia các hoạt động thể chất, hoạt động trải nghiệm, hoạt động xã hội và các sở thích cá nhân có thể tạo cơ hội để học sinh duy trì sự tập trung, phát triển các mối quan hệ trực tiếp và cân bằng việc sử dụng công nghệ.")

    with col2:
        st.markdown('<div class="nguyen-nhan-title">BIỂU HIỆN</div>', unsafe_allow_html=True)
        with st.expander("KHÓ DUY TRÌ SỰ CHÚ Ý ĐỐI VỚI CÁC NHIỆM VỤ KÉO DÀI"):
            st.write("Học sinh dễ mất tập trung khi thực hiện các hoạt động cần sự tập trung liên tục như đọc tài liệu dài, giải quyết vấn đề, làm bài tập hoặc tham gia các hoạt động học tập kéo dài.")
        with st.expander("DỄ MẤT KIÊN NHẪN"):
            st.write("Học sinh mong muốn nhận được kết quả hoặc phản hồi nhanh, gặp khó khăn khi phải chờ đợi hoặc thực hiện các nhiệm vụ cần đầu tư thời gian và nỗ lực.")
        with st.expander("THƯỜNG XUYÊN TÌM KIẾM CÁC KÍCH THÍCH MỚI"):
            st.write("Học sinh có xu hướng liên tục kiểm tra điện thoại, chuyển đổi giữa nhiều ứng dụng, nội dung hoặc hoạt động khác nhau trong thời gian ngắn.")
        with st.expander("CẢM GIÁC BỒN CHỒN KHI THIẾU KÍCH THÍCH SỐ"):
            st.write("Học sinh cảm thấy khó chịu, bứt rứt hoặc có nhu cầu cầm điện thoại ngay khi không có hoạt động giải trí số.")
        with st.expander("KHÓ TỰ ĐIỀU CHỈNH HÀNH VI SỬ DỤNG CÔNG NGHỆ"):
            st.write("Học sinh nhận thức được việc sử dụng điện thoại quá nhiều nhưng gặp khó khăn trong việc kiểm soát, cắt giảm hoặc thay đổi hành vi.")

    st.markdown("<br><h2>ĐÔI LỜI CHUYÊN GIA AI MUỐN GỬI ĐẾN BẠN</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="intro-text">
    <i>"Hãy học cách buông bỏ thiết bị công nghệ đúng lúc, dành thời gian cho những khoảng lặng tĩnh tâm và trân trọng từng khoảnh khắc trong thế giới thực. Sự tập trung sâu sắc chính là siêu năng lực giúp bạn làm chủ tri thức và cuộc sống của chính mình."</i>
    </div>
    """, unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200", caption="Cân bằng cuộc sống số và thế giới thực", use_container_width=True)

with tab2:
    st.markdown("""
    <div class="expert-card">
        <p>Nếu bạn muốn trò chuyện về vấn đề "não bỏng ngô" hoặc giải pháp để khắc phục nó thì hãy đến với chuyên gia Gen Z của chúng tôi ✨🍿</p>
    </div>
    """, unsafe_allow_html=True)

    # Khung đếm thời gian thủ công
    with st.expander("⏱️ BỘ ĐẾM THỜI GIAN THỬ THÁCH (DIGITAL DETOX TIMER)"):
        st.write("Chọn thời gian bạn muốn thử thách cất điện thoại hoặc tập trung chữa lành:")
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            timer_minutes = st.selectbox("Chọn số phút:", [3, 5, 10, 15, 20, 30], index=0)
        with col_t2:
            st.write("")
            st.write("")
            start_timer = st.button("🚀 Bắt đầu đếm ngược")

        if start_timer:
            timer_placeholder = st.empty()
            total_seconds = timer_minutes * 60
            while total_seconds > 0:
                mins, secs = divmod(total_seconds, 60)
                timer_placeholder.markdown(f"### ⏳ Thời gian thử thách còn lại: **{mins:02d}:{secs:02d}** 🔥")
                time.sleep(1)
                total_seconds -= 1
            timer_placeholder.markdown("### 🎉 🥳 Xuất sắc đỉnh chóp! Bạn đã hoàn thành thử thách. Quay lại chat với AI ngay nào! 💅✨")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input('Hé lô! Cần chuyên gia Gen Z tư vấn gì về "não bỏng ngô" không? 🍿🔥'):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not client:
                ai_reply = "⚠️ U là trời 🤦‍♂️! Bạn chưa điền API Key kìa. Hãy cấu hình `GEMINI_API_KEY` trong Streamlit Secrets nha ✨!"
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                ai_reply = None
                for attempt in range(3):
                    try:
                        system_instruction = """
                        Bạn là một trợ lý AI Gen Z chuyên gia chữa lành hội chứng "Popcorn Brain" (não bỏng ngô) cực kỳ thân thiện, lầy lội và tràn đầy năng lượng tích cực! 🔥✨
                        
                        QUY TẮC BẮT BUỘC:
                        1. KHI NGƯỜI DÙNG KHOE HOẶC HỎI VỀ VIỆC LƯỚT TIKTOK / MẠNG XÃ HỘI: Bạn PHẢI MẮNG MỎ, CẢNH TỈNH VÀ NGĂN CẢN NGAY LẬP TỨC bằng văn phong Gen Z cực lầy lội! Không đưa ra giải pháp vội.
                        2. KHI NGƯỜI DÙNG HỎI NGOÀI LỀ (giải toán, code, nấu ăn...): Từ chối lầy lội và giới thiệu sang bạn AI khác.
                        3. KHI NGƯỜI DÙNG CHỦ ĐỘNG HỎI CÁCH CHỮA/KHẮC PHỤC HOẶC ĐỒNG Ý LÀM THEO HƯỚNG DẪN: Đưa ra bước đầu tiên yêu cầu họ rời mắt khỏi màn hình/đứng dậy thư giãn, VÀ BẠN PHẢI ĐÍNH KÈM THẺ KÍCH HOẠT ĐỒNG HỒ Ở CUỐI CÂU TRẢ LỜI theo định dạng chính xác này: [START_TIMER:3] (với số 3 là số phút bấm giờ tương ứng).
                        4. PHẢI BẮN EMOJI NHIỆT TÌNH 🤪🍿📱⚡: Dùng từ lóng Gen Z ('keo lỳ', 'ét o ét', 'cháy quá', 'mấy ní'...)!
                        """
                        
                        chat_history = []
                        for msg in st.session_state.messages[:-1]:
                            role = "model" if msg["role"] == "assistant" else "user"
                            chat_history.append({"role": role, "parts": [{"text": msg["content"]}]})

                        chat = client.chats.create(model='gemini-3.5-flash-lite', history=chat_history)
                        response = chat.send_message(prompt, config={'system_instruction': system_instruction})
                        
                        ai_reply = response.text
                        break
                    except Exception as e:
                        if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < 2:
                            time.sleep(2)
                            continue
                        elif "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                            ai_reply = "Ét o ét 😭! API Key đã chạm giới hạn miễn phí rồi. Hãy tạo API key mới tại Google AI Studio nhé ⚡!"
                            break
                        else:
                            ai_reply = f"Ét o ét 😱, có lỗi xíu xiu rồi ní ơi: {e}"
                            break
                
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})

                # TỰ ĐỘNG BẬT BỘ ĐẾM NGƯỢC NẾU AI CÓ GỬI KÈM THẺ [START_TIMER:X]
                if "[START_TIMER:" in ai_reply:
                    try:
                        match = re.search(r'\[START_TIMER:(\d+)\]', ai_reply)
                        if match:
                            minutes = int(match.group(1))
                            st.markdown(f"### ⏱️ Kích hoạt thử thách {minutes} phút chữa lành:")
                            timer_placeholder = st.empty()
                            total_seconds = minutes * 60
                            while total_seconds > 0:
                                mins, secs = divmod(total_seconds, 60)
                                timer_placeholder.markdown(f"### ⏳ Thời gian thử thách còn lại: **{mins:02d}:{secs:02d}** 🔥")
                                time.sleep(1)
                                total_seconds -= 1
                            timer_placeholder.markdown("### 🎉 🥳 Xuất sắc đỉnh chóp! Bạn đã hoàn thành thử thách. Báo cáo ngay cho chuyên gia nào! 💅✨")
                    except Exception as timer_err:
                        st.write(f"Lỗi chạy đồng hồ: {timer_err}")
