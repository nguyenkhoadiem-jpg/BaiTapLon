from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import schedule
import datetime

def init_driver():
    """Khởi tạo trình duyệt Chrome với user-agent."""
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    return webdriver.Chrome(options=options)

def get_page_data(driver):
    """
    Thu thập dữ liệu từ trang chủ Kenh14.vn
    Trả về danh sách bài viết.
    """
    url = "https://kenh14.vn/"
    print(f"Đang crawl Kenh14.vn...")
    driver.get(url)
    time.sleep(3)

    data = []
    articles = driver.find_elements(By.CSS_SELECTOR, "div.knswli-right")

    if not articles:
        print("Không tìm thấy bài viết nào.")
        return data

    for article in articles:
        try:
            title = article.find_element(By.CSS_SELECTOR, "h3.knswli-title a").text.strip()
            link = article.find_element(By.CSS_SELECTOR, "h3.knswli-title a").get_attribute("href")
            summary = article.find_element(By.CSS_SELECTOR, "div.knswli-sapo").text.strip()
            data.append([title, summary, link])
        except:
            continue
    
    return data

def save_to_excel(data):
    """Lưu dữ liệu vào file Excel theo ngày hiện tại."""
    today = datetime.datetime.now().strftime("%Y%m%d")
    df = pd.DataFrame(data, columns=["Tiêu đề", "Tóm tắt", "Link"])
    output_file = f"kenh14_baiviet_{today}.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Đã lưu {len(data)} bài viết vào {output_file}")

def crawl_kenh14():
    """Hàm chính để crawl dữ liệu bài viết từ kenh14.vn."""
    driver = init_driver()
    try:
        data = get_page_data(driver)
        save_to_excel(data)
    finally:
        driver.quit()

if _name_ == "_main_":
    schedule.every().day.at("06:00").do(crawl_kenh14)
    print("Đã lên lịch crawl Kenh14 lúc 6:00 .")
    while True:
        schedule.run_pending()
        time.sleep(60)