# Quiz Application - Selenium Testing Guide

## Application Overview

This is a Dynamic Quiz Application built with React, TypeScript, and Tailwind CSS. The application features:
- Multiple quiz categories (Programming, Science, History, Geography, Math, General Knowledge)
- Three difficulty levels (Easy, Medium, Hard)
- Countdown timer for each question
- Dynamic question navigation
- Detailed result analysis with charts

## Application Structure

### Key Components

1. **QuizHome** - Landing page with category and difficulty selection
2. **QuizInterface** - Quiz questions with timer and navigation
3. **QuizResults** - Result analysis with charts and detailed breakdown

### Important Element IDs for Selenium Testing

The following IDs have been added to key elements for easy Selenium automation:

#### Home Page
- `start-quiz-button` - Start Quiz button (visible after selecting category and difficulty)

#### Quiz Interface
- `question-nav-{number}` - Question navigation dots (e.g., `question-nav-1`, `question-nav-2`)
- `question-{number}` - Question text (e.g., `question-1`, `question-2`)
- `option-{number}` - Answer options (1-4 for each question)
- `submit-quiz-button` - Submit Quiz button (visible on last question)

#### Results Page
- `score-percentage` - Final score percentage
- `correct-answers` - Number of correct answers
- `incorrect-answers` - Number of incorrect answers

## Selenium Test Scenarios

### Test Case 1: Complete Quiz Flow

```java
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

public class QuizAutomationTest {
    
    WebDriver driver;
    WebDriverWait wait;
    
    @Before
    public void setup() {
        // Set up ChromeDriver
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        driver.manage().window().maximize();
    }
    
    @Test
    public void testCompleteQuizFlow() {
        // Step 1: Navigate to quiz application
        driver.get("YOUR_QUIZ_URL_HERE");
        System.out.println("Current URL: " + driver.getCurrentUrl());
        System.out.println("Page Title: " + driver.getTitle());
        
        // Step 2: Select category (Programming)
        WebElement categoryCard = wait.until(ExpectedConditions.elementToBeClickable(
            By.xpath("//h3[contains(text(), 'Programming')]/ancestor::div[contains(@class, 'cursor-pointer')]")
        ));
        categoryCard.click();
        Thread.sleep(500);
        
        // Step 3: Select difficulty (Easy)
        WebElement difficultyCard = wait.until(ExpectedConditions.elementToBeClickable(
            By.xpath("//h3[contains(text(), 'Easy')]/ancestor::div[contains(@class, 'cursor-pointer')]")
        ));
        difficultyCard.click();
        Thread.sleep(500);
        
        // Step 4: Click Start Quiz button
        WebElement startButton = wait.until(ExpectedConditions.elementToBeClickable(
            By.id("start-quiz-button")
        ));
        startButton.click();
        System.out.println("Quiz started successfully");
        
        // Step 5: Answer questions
        // For Programming - Easy, there are 3 questions
        int[] answers = {0, 2, 1}; // Answer indices for each question (0-based)
        
        for (int i = 0; i < answers.length; i++) {
            // Wait for question to load
            WebElement question = wait.until(ExpectedConditions.presenceOfElementLocated(
                By.id("question-" + (i + 1))
            ));
            System.out.println("Question " + (i + 1) + ": " + question.getText());
            
            // Select answer
            WebElement option = wait.until(ExpectedConditions.elementToBeClickable(
                By.id("option-" + (answers[i] + 1))
            ));
            option.click();
            System.out.println("Selected option: " + (answers[i] + 1));
            
            // Wait a bit for the answer to be processed
            Thread.sleep(1000);
            
            // Click Next or Submit button
            if (i < answers.length - 1) {
                WebElement nextButton = driver.findElement(
                    By.xpath("//button[contains(., 'Next')]")
                );
                nextButton.click();
            } else {
                WebElement submitButton = driver.findElement(By.id("submit-quiz-button"));
                submitButton.click();
            }
            
            Thread.sleep(500);
        }
        
        // Step 6: Verify results page
        WebElement scoreElement = wait.until(ExpectedConditions.presenceOfElementLocated(
            By.id("score-percentage")
        ));
        String score = scoreElement.getText();
        System.out.println("Final Score: " + score);
        
        WebElement correctAnswers = driver.findElement(By.id("correct-answers"));
        System.out.println("Correct Answers: " + correctAnswers.getText());
        
        WebElement incorrectAnswers = driver.findElement(By.id("incorrect-answers"));
        System.out.println("Incorrect Answers: " + incorrectAnswers.getText());
        
        // Verify score is displayed
        assertTrue("Score should be displayed", !score.isEmpty());
        System.out.println("Test completed successfully!");
    }
    
    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
```

### Test Case 2: Question Navigation Test

```java
@Test
public void testQuestionNavigation() {
    // Navigate to quiz and start
    driver.get("YOUR_QUIZ_URL_HERE");
    
    // Select category and difficulty
    driver.findElement(By.xpath("//h3[contains(text(), 'Science')]/ancestor::div[contains(@class, 'cursor-pointer')]")).click();
    Thread.sleep(500);
    driver.findElement(By.xpath("//h3[contains(text(), 'Medium')]/ancestor::div[contains(@class, 'cursor-pointer')]")).click();
    Thread.sleep(500);
    driver.findElement(By.id("start-quiz-button")).click();
    
    // Test navigation dots
    for (int i = 1; i <= 3; i++) {
        WebElement navDot = wait.until(ExpectedConditions.elementToBeClickable(
            By.id("question-nav-" + i)
        ));
        navDot.click();
        Thread.sleep(500);
        
        WebElement question = driver.findElement(By.id("question-" + i));
        System.out.println("Navigated to Question " + i + ": " + question.getText());
    }
}
```

### Test Case 3: Timer Verification

```java
@Test
public void testTimerFunctionality() {
    // Start quiz
    driver.get("YOUR_QUIZ_URL_HERE");
    driver.findElement(By.xpath("//h3[contains(text(), 'Math')]/ancestor::div[contains(@class, 'cursor-pointer')]")).click();
    Thread.sleep(500);
    driver.findElement(By.xpath("//h3[contains(text(), 'Easy')]/ancestor::div[contains(@class, 'cursor-pointer')]")).click();
    Thread.sleep(500);
    driver.findElement(By.id("start-quiz-button")).click();
    
    // Wait for question to load
    wait.until(ExpectedConditions.presenceOfElementLocated(By.id("question-1")));
    
    // Find timer element
    WebElement timer = driver.findElement(By.xpath("//span[contains(@class, 'font-bold') and contains(text(), 's')]"));
    String initialTime = timer.getText().replace("s", "");
    System.out.println("Initial timer: " + initialTime);
    
    // Wait and check timer again
    Thread.sleep(3000);
    String laterTime = timer.getText().replace("s", "");
    System.out.println("Timer after 3 seconds: " + laterTime);
    
    // Verify timer is counting down
    assertTrue("Timer should count down", Integer.parseInt(laterTime) < Integer.parseInt(initialTime));
}
```

## Screenshot Points

Take screenshots at these key moments:
1. Landing page with categories
2. After selecting category
3. After selecting difficulty
4. First question displayed
5. After selecting an answer
6. Timer warning (when < 10 seconds)
7. Question navigation dots
8. Last question with Submit button
9. Results page with score
10. Charts on results page

## Logging Best Practices

```java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class QuizAutomationTest {
    private static final Logger logger = LogManager.getLogger(QuizAutomationTest.class);
    
    @Test
    public void testWithLogging() {
        logger.info("Starting quiz automation test");
        
        try {
            driver.get(URL);
            logger.info("Navigated to URL: " + driver.getCurrentUrl());
            
            // Take screenshot
            File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
            FileUtils.copyFile(screenshot, new File("screenshots/landing-page.png"));
            logger.info("Screenshot saved: landing-page.png");
            
            // Continue with test...
            
        } catch (Exception e) {
            logger.error("Test failed: " + e.getMessage(), e);
            // Take error screenshot
            File errorScreenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
            FileUtils.copyFile(errorScreenshot, new File("screenshots/error.png"));
        }
    }
}
```

## Answer Key for Testing

### Programming - Easy
1. What does HTML stand for? → **A** (Hyper Text Markup Language)
2. Which programming language is known as the 'language of the web'? → **C** (JavaScript)
3. What does CSS stand for? → **B** (Cascading Style Sheets)

### Science - Easy
1. What is the chemical symbol for water? → **A** (H2O)
2. What planet is known as the Red Planet? → **C** (Mars)
3. What force keeps us on the ground? → **C** (Gravity)

### Math - Easy
1. What is 15 + 27? → **B** (42)
2. What is 8 × 7? → **B** (56)
3. What is the square root of 64? → **C** (8)

## Recording Setup

For screen recording during test execution:

### Windows
- Use OBS Studio or Windows Game Bar (Win + G)

### Mac
- Use QuickTime Player or built-in screen recording (Cmd + Shift + 5)

### Linux
- Use SimpleScreenRecorder or Kazam

## Test Execution Steps

1. **Preparation**
   - Start your web application
   - Set up ChromeDriver path
   - Configure logging
   - Start screen recording

2. **Execution**
   - Run Selenium tests
   - Monitor console output
   - Check for errors

3. **Post-Execution**
   - Stop screen recording
   - Collect screenshots
   - Generate test report
   - Review logs

## Deliverables Checklist

- [ ] Screen recording of complete test execution
- [ ] Screenshots at each significant step
- [ ] Selenium logs documenting all interactions
- [ ] Test report with results summary
- [ ] GitHub repository with automation code
- [ ] Drive link to all test artifacts

## Notes

- All questions have 4 answer options (A, B, C, D)
- Timer varies by difficulty: Easy (20s), Medium (25s), Hard (30s)
- Auto-submit occurs when timer reaches 0
- Results show detailed breakdown with charts
- Application is fully responsive (desktop, tablet, mobile)
