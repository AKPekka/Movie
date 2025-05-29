# 1) Front-end builder
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/movie-recommendation-ui/package*.json ./
RUN npm ci
COPY frontend/movie-recommendation-ui .
RUN npm run build

# 2) Back-end builder
FROM python:3.10-slim AS backend-builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend .

# 3) Final image (run both)
FROM python:3.10-slim
WORKDIR /app

# copy Python libs & backend code
COPY --from=backend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=backend-builder /app /app

# copy React build into a folder your Flask app can serve
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# if your Flask app is set up like:
#   app = Flask(__name__, static_folder="frontend/build", static_url_path="")
#    @app.route("/")
#    def index(): return app.send_static_file("index.html")
# then React will be automatically served.

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
