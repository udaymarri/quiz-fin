# 🎯 QuizMaster Pro - Dynamic Quiz Application

A stunning, feature-rich quiz application built with React, TypeScript, Tailwind CSS, and Motion animations. Test your knowledge across 6 categories with timed challenges and detailed analytics.

![QuizMaster Pro](https://img.shields.io/badge/QuizMaster-Pro-blueviolet?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.3.1-61dafb?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.1-38bdf8?style=for-the-badge&logo=tailwind-css)

## ✨ Features

### 🎨 **Premium UI/UX**
- Glassmorphism effects with animated blob backgrounds
- Smooth page transitions with Motion animations
- Responsive design for all devices
- Gradient color schemes (blue-indigo-purple-pink)
- Interactive floating quiz icons
- Confetti animations for high scores

### 📚 **Quiz Categories (57 Questions)**
- 💻 **Programming** (11 questions)
- 🔬 **Science** (10 questions)
- 📚 **History** (9 questions)
- 🌍 **Geography** (9 questions)
- 🔢 **Mathematics** (9 questions)
- 🧠 **General Knowledge** (9 questions)

### ⚡ **Difficulty Levels**
- 🟢 **Easy** - 20 seconds per question
- 🟡 **Medium** - 25 seconds per question
- 🔴 **Hard** - 30 seconds per question

### 📊 **Advanced Features**
- Circular SVG countdown timer
- Question-by-question navigation
- Automatic submission on timeout
- Detailed result analysis with charts (Recharts)
- Time tracking per question
- Performance metrics and scoring
- Pie charts and bar graphs
- Question-by-question breakdown

### 🧪 **Testing Ready**
- All components have Selenium WebDriver IDs
- Automated testing support
- Clean component structure

## 🚀 Tech Stack

- **Framework:** React 18.3.1
- **Language:** TypeScript
- **Styling:** Tailwind CSS 4.1
- **Animations:** Motion (Framer Motion) 12.23
- **Charts:** Recharts 2.15
- **Icons:** Lucide React
- **UI Components:** Radix UI
- **Build Tool:** Vite 6.3

## 📦 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd quizmaster-pro

# Install dependencies (using npm)
npm install

# Or using pnpm
pnpm install

# Or using yarn
yarn install
```

## 🛠️ Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The application will be available at `http://localhost:5173`

## 📁 Project Structure

```
quizmaster-pro/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── LandingPage.tsx          # Landing page with animations
│   │   │   ├── QuizHome.tsx             # Category & difficulty selection
│   │   │   ├── QuizInterface.tsx        # Main quiz interface
│   │   │   ├── QuizResults.tsx          # Results page with charts
│   │   │   └── ui/                      # Reusable UI components
│   │   ├── data/
│   │   │   └── quizData.ts              # All 57 quiz questions
│   │   ├── utils/
│   │   │   └── validateQuizData.ts      # Data validation utility
│   │   └── App.tsx                      # Main app component
│   ├── styles/
│   │   ├── index.css                    # Main styles
│   │   ├── tailwind.css                 # Tailwind config
│   │   ├── theme.css                    # Theme variables
│   │   └── fonts.css                    # Font imports
│   └── main.tsx                         # Entry point
├── index.html                           # HTML template
├── vite.config.ts                       # Vite configuration
├── vercel.json                          # Vercel deployment config
└── package.json                         # Dependencies
```

## 🎮 How to Use

1. **Landing Page** - Click "Start Your Journey" to enter
2. **Select Category** - Choose from 6 available categories
3. **Select Difficulty** - Pick Easy, Medium, or Hard
4. **Take Quiz** - Answer questions before time runs out
5. **View Results** - See detailed analytics and performance metrics

## 🌟 Key Components

### LandingPage
- Premium animated background with floating icons
- Interactive statistics display
- Smooth entrance animations

### QuizHome
- Category selection with gradient cards
- Difficulty level selection
- Animated feature banners

### QuizInterface
- Circular SVG timer with color-coded warnings
- Question navigation system
- Real-time answer validation
- Automatic progression

### QuizResults
- Score percentage calculation
- Time spent analysis
- Bar chart for question timing
- Pie chart for answer distribution
- Detailed question-by-question breakdown
- Confetti animation for good scores

## 📊 Question Distribution

Each category has questions distributed across three difficulty levels:

| Category | Easy | Medium | Hard | Total |
|----------|------|--------|------|-------|
| Programming | 3 | 5 | 3 | 11 |
| Science | 3 | 5 | 2 | 10 |
| History | 3 | 4 | 2 | 9 |
| Geography | 3 | 4 | 2 | 9 |
| Mathematics | 3 | 4 | 2 | 9 |
| General Knowledge | 3 | 4 | 2 | 9 |
| **Total** | **18** | **26** | **13** | **57** |

## 🎨 Animations & Effects

- **Blob Animation** - Organic floating background shapes
- **Page Transitions** - Smooth Motion-powered transitions
- **Hover Effects** - Interactive cards and buttons
- **Timer Animation** - Circular SVG countdown
- **Confetti** - Celebration effect for high scores
- **Shimmer Effects** - Premium hover interactions
- **3D Parallax** - Mouse-tracking effects on landing page

## 🔧 Configuration

### Vite Config
The project uses Vite with React and Tailwind plugins. Path aliases are configured for clean imports.

### Vercel Config
Pre-configured for seamless Vercel deployment with SPA routing support.

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👨‍💻 Author

Built with ❤️ for quiz enthusiasts everywhere

## 🙏 Acknowledgments

- React Team for the amazing framework
- Tailwind CSS for utility-first styling
- Motion for smooth animations
- Radix UI for accessible components
- Recharts for beautiful data visualization

---

**Made with 💜 by QuizMaster Pro Team**

⭐ Star this repo if you find it helpful!
