# Cài đặt thư viện Python
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp requirements.txt và cài đặt các dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Cài đặt biến môi trường để tránh buffering logs
ENV PYTHONUNBUFFERED=1

# Mở cổng cho ứng dụng
EXPOSE 8000

# Lệnh khởi động ứng dụng FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
