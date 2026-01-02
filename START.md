# 🚀 How to Start RepBot WebApp

## Quick Start Guide

You need to start **TWO servers** - Backend and Frontend. Both must be running at the same time!

---

## 📋 Step 1: Start Backend Server

### Option A: Using Batch File (Easiest)
1. Double-click: `backend\start.bat`
2. Wait for it to start (you'll see "Running on http://0.0.0.0:5000")

### Option B: Manual Start
1. Open **PowerShell** or **Command Prompt**
2. Navigate to backend:
   ```bash
   cd backend
   ```
3. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
4. Start server:
   ```bash
   python app.py
   ```

**✅ Success:** You should see:
```
✓ MediaPipe imported successfully
✓ ML Pipeline initialized successfully
* Running on http://0.0.0.0:5000
```

**⚠️ Keep this terminal open!**

---

## 📋 Step 2: Start Frontend Server

### Option A: Using Batch File (Easiest)
1. Double-click: `frontend\start.bat`
2. Wait for it to start

### Option B: Manual Start
1. Open a **NEW** terminal window
2. Navigate to frontend:
   ```bash
   cd frontend
   ```
3. Start server:
   ```bash
   npm run dev
   ```

**✅ Success:** You should see:
```
VITE v7.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

**⚠️ Keep this terminal open too!**

---

## 📋 Step 3: Open in Browser

1. Open your web browser (Chrome, Edge, Firefox)
2. Go to: **http://localhost:5173**
3. You should see the RepBot login page!

---

## 🎯 Quick Reference

### Terminal 1 (Backend):
```bash
cd backend
venv\Scripts\activate
python app.py
```
**Status:** Should show "Running on http://0.0.0.0:5000"

### Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```
**Status:** Should show "Local: http://localhost:5173/"

### Browser:
- URL: **http://localhost:5173**

---

## ✅ Checklist

Before using Live Exercise feature:

- [ ] Backend server running (shows "Running on http://0.0.0.0:5000")
- [ ] Frontend server running (shows "Local: http://localhost:5173/")
- [ ] Browser open at http://localhost:5173
- [ ] Camera is connected to your computer

---

## 🎮 Using Live Exercise

1. In the browser, click **"Start Workout"** or navigate to **"Live Exercise"**
2. Select an exercise (Bicep Curl, Squat, Push Up, etc.)
3. Click the **"START"** button
4. Allow camera access if prompted
5. Position yourself in front of the camera
6. Start exercising - you'll see:
   - Real-time video with pose detection
   - Rep counting
   - Form feedback
   - Confidence scores

---

## 🛑 Stopping Servers

To stop:
1. Go to each terminal
2. Press `Ctrl + C`
3. Confirm if asked

---

## 🐛 Troubleshooting

### Backend won't start?
- Check: Virtual environment activated? (should see `(venv)` in prompt)
- Check: MediaPipe installed? Run `python -c "import mediapipe"`
- Check: Port 5000 free? Close other apps using it

### Frontend won't start?
- Check: Dependencies installed? Run `npm install` in frontend folder
- Check: Port 5173 free? Vite will use next available port

### Webcam not working?
- Check: Backend terminal shows "Camera started"
- Check: No other app using camera
- Check: Camera permissions in Windows

---

## 📁 Important Files

- **Backend:** `backend\app.py` - Main Flask server
- **Frontend:** `frontend\` - React application
- **Start Backend:** `backend\start.bat`
- **Start Frontend:** `frontend\start.bat`

---

**Both servers must be running!** 🚀


