import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { LandingPage } from '@/app/components/LandingPage';
import { QuizHome } from '@/app/components/QuizHome';
import { QuizInterface, QuizResult } from '@/app/components/QuizInterface';
import { QuizResults } from '@/app/components/QuizResults';
import { getQuestionsByCategory } from '@/app/data/quizData';

type AppState = 'landing' | 'home' | 'quiz' | 'results';

function App() {
  const [appState, setAppState] = useState<AppState>('landing');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('');
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);

  const handleEnterApp = () => {
    setAppState('home');
  };

  const handleStartQuiz = (category: string, difficulty: string) => {
    setSelectedCategory(category);
    setSelectedDifficulty(difficulty);
    setAppState('quiz');
  };

  const handleQuizComplete = (result: QuizResult) => {
    setQuizResult(result);
    setAppState('results');
  };

  const handleRetakeQuiz = () => {
    setAppState('quiz');
  };

  const handleGoHome = () => {
    setAppState('home');
    setSelectedCategory('');
    setSelectedDifficulty('');
    setQuizResult(null);
  };

  const questions = getQuestionsByCategory(selectedCategory, selectedDifficulty);

  const pageVariants = {
    initial: { opacity: 0, scale: 0.95, y: 20 },
    animate: { opacity: 1, scale: 1, y: 0 },
    exit: { opacity: 0, scale: 0.95, y: -20 }
  };

  const pageTransition = {
    type: "spring",
    stiffness: 300,
    damping: 30,
    duration: 0.4
  };

  return (
    <div className="min-h-screen">
      <AnimatePresence mode="wait">
        {appState === 'landing' && (
          <motion.div
            key="landing"
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={pageTransition}
          >
            <LandingPage onEnter={handleEnterApp} />
          </motion.div>
        )}
        
        {appState === 'home' && (
          <motion.div
            key="home"
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={pageTransition}
          >
            <QuizHome onStartQuiz={handleStartQuiz} />
          </motion.div>
        )}
        
        {appState === 'quiz' && questions.length > 0 && (
          <motion.div
            key="quiz"
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={pageTransition}
          >
            <QuizInterface
              questions={questions}
              category={selectedCategory}
              difficulty={selectedDifficulty}
              onComplete={handleQuizComplete}
            />
          </motion.div>
        )}
        
        {appState === 'results' && quizResult && (
          <motion.div
            key="results"
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={pageTransition}
          >
            <QuizResults
              result={quizResult}
              onRetakeQuiz={handleRetakeQuiz}
              onGoHome={handleGoHome}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;