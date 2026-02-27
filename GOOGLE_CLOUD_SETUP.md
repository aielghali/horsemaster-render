# 🚀 HorseMaster AI - Google Cloud Setup Guide

## الطريقة السريعة (نسخ ولصق)

### الخطوة 1: افتح Google Cloud Shell
1. اذهب إلى: https://console.cloud.google.com
2. اضغط على أيقونة **Terminal/Cloud Shell** في أعلى اليمين (>_)

### الخطوة 2: انسخ والصق هذا الأمر
```bash
curl -sSL https://raw.githubusercontent.com/aielghali/horsemaster-render/master/setup-gcloud.sh | bash
```

---

## الطريقة اليدوية (خطوة بخطوة)

### 1️⃣ إنشاء المشروع
```bash
# إنشاء مشروع جديد
gcloud projects create horsemaster-ai-$(date +%Y%m%d) --name="HorseMaster AI"

# تحديد المشروع
gcloud config set project horsemaster-ai-$(date +%Y%m%d)
```

### 2️⃣ ربط حساب الدفع
- اذهب إلى: https://console.cloud.google.com/billing
- اربط بطاقة ائتمان (لن يتم خصم شيء - Free Tier يكفي)

### 3️⃣ تفعيل APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 4️⃣ استنساخ المشروع
```bash
git clone https://github.com/aielghali/horsemaster-render.git
cd horsemaster-render
```

### 5️⃣ تعيين الأذونات
```bash
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/storage.admin"
```

### 6️⃣ البناء والنشر
```bash
PROJECT_ID=$(gcloud config get-value project)

# بناء الصورة
gcloud builds submit --tag gcr.io/$PROJECT_ID/horsemaster

# نشر على Cloud Run
gcloud run deploy horsemaster \
    --image gcr.io/$PROJECT_ID/horsemaster \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512Mi \
    --min-instances 0 \
    --max-instances 3
```

### 7️⃣ الحصول على الرابط
```bash
gcloud run services describe horsemaster \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)'
```

---

## 🔗 إعداد النشر التلقائي من GitHub

1. اذهب إلى: https://console.cloud.google.com/cloud-build/triggers
2. اضغط **"Create Trigger"**
3. أدخل المعلومات:
   - **Name:** `horsemaster-auto-deploy`
   - **Event:** Push to a branch
   - **Source:** GitHub
   - **Repository:** aielghali/horsemaster-render
   - **Branch:** `^master$`
   - **Configuration:** Existing Cloud Build configuration file
   - **Location:** `cloudbuild.yaml`
4. اضغط **"Create"**

---

## 📊 مقارنة: Render vs Google Cloud Run

| الميزة | Render | Google Cloud Run |
|--------|--------|------------------|
| السرعة | بطيء (Free) | ⚡ سريع |
| السكون | ينام بعد 15 دقيقة | لا ينام |
| الاستجابة الباردة | 30-60 ثانية | 1-5 ثواني |
| التكلفة | مجاني | مجاني (Free Tier) |

---

## ✅ اختبار التطبيق

```bash
# احصل على الرابط
URL=$(gcloud run services describe horsemaster --platform managed --region us-central1 --format 'value(status.url)')

# اختبار Health Check
curl $URL/health

# اختبار واجهة الويب
echo "Open: $URL"
```

---

## 🆘 حل المشاكل

### مشكلة: "Permission denied"
```bash
# منح الأذونات مرة أخرى
gcloud auth application-default login
```

### مشكلة: "Billing not enabled"
- اذهب إلى Console واربط بطاقة الائتمان

### مشكلة: "Quota exceeded"
- Free Tier محدود، انتظر 24 ساعة أو قلل الاستخدام
