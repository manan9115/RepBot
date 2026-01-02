# RepBot - AI-Assisted Fitness Tracker

A modern web application for tracking workouts, monitoring exercise form, and managing diet plans with AI-powered pose detection capabilities. **Now integrated with RepBot backend for real-time MediaPipe/OpenCV-based exercise tracking and form validation!**

## 🚀 Features

- **User Authentication**: Secure login and signup with session management
- **Dashboard**: Overview of workout stats, heart rate, calories, and activity time
- **Live Exercise Tracking**: Real-time webcam-based exercise monitoring with MediaPipe pose detection
- **Real-time Rep Counting**: Automatic rep counting for Bicep Curls, Squats, and Lateral Raises
- **Form Validation**: ML-powered form analysis using local models and enhanced validation
- **Workout Summary**: Detailed analytics and progress tracking with visual charts
- **Diet Planner**: BMI calculator with personalized diet plans based on body metrics
- **Responsive Design**: Modern UI built with React, Tailwind CSS, and Recharts

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 16 or higher) - [Download here](https://nodejs.org/)
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **npm** (comes with Node.js) or **yarn**
- A modern web browser (Chrome, Firefox, Edge, Safari)
- Webcam (for live exercise tracking feature)
- **RTX 2050 GPU** (optional, for enhanced performance)

## 🛠️ Installation & Setup

### Backend Setup (Required for Live Exercise Tracking)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Linux/Mac**: `source venv/bin/activate`

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (CORS support)
- OpenCV (computer vision)
- MediaPipe (pose detection)
- scikit-learn (ML models)
- transformers (Hugging Face models)
- And other dependencies

5. Verify model files are present:
   - `exercise_form_model.pkl` (optional, for enhanced form validation)
   - `scaler.pkl` (optional, for model preprocessing)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

This will install all required packages including:
- React 19
- React Router DOM
- Recharts (for data visualization)
- Tailwind CSS
- React Icons
- And other dependencies

3. Verify Installation:
Check that `node_modules` folder was created and all packages are installed correctly.

## 🎯 Running the Application

**👉 See [START.md](START.md) for detailed step-by-step instructions!**

### Quick Start:

1. **Start Backend:** Double-click `backend\start.bat` or run `python app.py` in backend folder
2. **Start Frontend:** Double-click `frontend\start.bat` or run `npm run dev` in frontend folder
3. **Open Browser:** Go to http://localhost:5173

### Important Notes:
- **Both servers must be running** for the Live Exercise feature to work
- The backend handles camera access and pose detection
- The frontend connects to the backend API for real-time data

### Building for Production

To create a production build:

```bash
npm run build
```

The optimized files will be in the `dist` folder.

### Preview Production Build

To preview the production build locally:

```bash
npm run preview
```

## 📱 Using the Application

### 1. **Sign Up / Login**
   - Navigate to the login page
   - Click "Sign Up" to create a new account
   - Or use any email/password to login (currently using mock authentication)
   - Check "Remember Me" to persist your session

### 2. **Dashboard**
   - View your workout statistics
   - See weekly progress charts
   - Access quick actions for workouts and diet planning

### 3. **Live Exercise** (Requires Backend Running)
   - **Make sure the backend server is running** (see Running the Application)
   - Click "Start Workout" from the dashboard
   - Select an exercise type (Bicep Curl, Squat, or Lateral Raise)
   - Click "START" to begin tracking
   - The system will:
     - Stream video with real-time pose detection
     - Automatically count reps based on movement patterns
     - Validate exercise form using ML models
     - Display real-time feedback and confidence scores
   - Monitor your reps, sets, and form in real-time

### 4. **Workout Summary**
   - View detailed analytics after completing a workout
   - See exercise type breakdown
   - Check consistency and improvement metrics

### 5. **Diet Planner**
   - Enter your height, weight, age, and gender
   - Calculate your BMI
   - Get personalized diet plans with meal breakdowns
   - View nutritional charts

## 🐛 Troubleshooting

### Backend Not Connected
- **Issue**: "Backend server is not running" error in frontend
- **Solution**: 
  - Make sure the Flask backend is running on port 5000
  - Check that Python dependencies are installed correctly
  - Verify camera is connected and accessible
  - Check backend terminal for error messages

### Webcam Not Working
- **Issue**: "Unable to access webcam" error
- **Solution**: 
  - Check that backend server is running
  - Ensure no other application is using the webcam
  - Try changing camera index in `backend/app.py` (currently 0)
  - Check camera permissions in your OS settings
  - Restart both frontend and backend servers

### Model Files Not Found
- **Issue**: Form validation not working optimally
- **Solution**:
  - The system works without model files using angle-based validation
  - For enhanced validation, ensure `exercise_form_model.pkl` and `scaler.pkl` are in the backend directory
  - These files should have been copied from the RepBot project

### Port Already in Use
- **Issue**: Port 5173 is already in use
- **Solution**: 
  - Kill the process using the port, or
  - Vite will automatically use the next available port

### Dependencies Installation Fails
- **Issue**: `npm install` fails
- **Solution**:
  - Clear npm cache: `npm cache clean --force`
  - Delete `node_modules` and `package-lock.json`
  - Run `npm install` again
  - Ensure you have Node.js 16+ installed

### Build Errors
- **Issue**: Build fails with errors
- **Solution**:
  - Check Node.js version: `node --version` (should be 16+)
  - Update npm: `npm install -g npm@latest`
  - Clear cache and reinstall dependencies

## 📁 Project Structure

```
RepBot-WebApp/
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   │   └── ProtectedRoute.jsx
│   │   ├── context/          # React Context providers
│   │   │   └── AuthContext.jsx
│   │   ├── pages/            # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── LiveExercise.jsx  # Integrated with backend
│   │   │   ├── WorkoutSummary.jsx
│   │   │   └── Diet.jsx
│   │   ├── App.jsx           # Main app component
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── public/               # Static assets
│   ├── index.html            # HTML template
│   ├── package.json          # Dependencies
│   ├── vite.config.js        # Vite configuration
│   └── tailwind.config.js    # Tailwind CSS config
└── backend/                  # Flask Backend API
    ├── app.py                # Main Flask application
    ├── pose_model.py         # MediaPipe pose detection
    ├── exercise_form_model.pkl  # ML model for form validation
    ├── scaler.pkl            # Feature scaler
    ├── requirements.txt      # Python dependencies
    ├── README.md            # Backend documentation
    └── start_backend.bat    # Windows startup script
```

## 🔧 Technology Stack

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 7
- **Routing**: React Router DOM 7
- **Styling**: Tailwind CSS 3
- **Charts**: Recharts 3
- **Icons**: React Icons

### Backend
- **Framework**: Flask 3.0
- **Computer Vision**: OpenCV 4.8
- **Pose Detection**: MediaPipe 0.10
- **ML/AI**: scikit-learn, Transformers (Hugging Face)
- **Video Processing**: Real-time MJPEG streaming

## 🎨 Features in Detail

### Authentication
- Mock authentication system (ready for backend integration)
- Session persistence with localStorage/sessionStorage
- Protected routes for authenticated users

### Live Exercise Tracking
- **Real-time pose detection** using MediaPipe
- **Automatic rep counting** for Bicep Curls, Squats, and Lateral Raises
- **ML-powered form validation** using local models and enhanced algorithms
- **Real-time video streaming** from backend with pose overlay
- **Form feedback** with confidence scores
- Set and rep progress tracking
- Real-time metrics (heart rate, calories, duration)
- Exercise selection and switching

### Dashboard Analytics
- Weekly progress visualization
- Quick stats cards
- Interactive charts with Recharts

### Diet Planning
- BMI calculation
- Personalized diet plans based on BMI categories
- Meal breakdown with macronutrients
- Visual charts for nutritional data

## 🚧 Future Enhancements

- [x] Integrate MediaPipe/OpenCV for real rep counting ✅
- [x] Backend API integration ✅
- [x] Complete rep counting for all 10 exercises ✅
- [x] Enhanced exercise detection for all exercise types ✅
- [x] Improved video element implementation ✅
- [x] Comprehensive angle calculations for better accuracy ✅
- [ ] Database for storing workout history
- [ ] User profile management
- [ ] Enhanced Hugging Face model integration
- [ ] Social sharing features
- [ ] Mobile app version
- [ ] Workout recommendations
- [ ] GPU acceleration optimization

## 📝 Notes

- Currently uses mock authentication (any email/password works)
- **Backend must be running** for Live Exercise feature to work
- Webcam access is handled by the backend (no browser permissions needed)
- Real-time pose detection uses MediaPipe (more accurate than TensorFlow.js for this use case)
- Form validation combines angle-based rules with ML model predictions
- The system automatically detects exercise type based on movement patterns
- GPU acceleration can be enabled for better performance (RTX 2050 supported)

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

This project is for personal/educational use.

---

**Happy Workout! 💪**

For issues or questions, check the troubleshooting section above or review the code comments.


