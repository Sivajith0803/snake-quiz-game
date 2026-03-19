# 🐍 Snake Quiz Game

An interactive, educational twist on the classic Snake arcade game. Built entirely in Python, this project challenges players to test their knowledge while managing the ever-growing length of their snake.

## 🎮 How to Play
1. **The Question:** A trivia question is displayed on the game screen.
2. **The Goal:** Navigate the snake toward the "food" that represents the **correct answer**.
3. **The Challenge:** - Consuming the correct answer increases your score and snake length.
   - Hitting a wall, your own tail, or an incorrect answer ends the game.
4. **High Scores:** Your best performance is saved locally in `highscore.txt`.

## 🛠️ Technical Features
- **100% Python Logic:** Handles game physics, collision detection, and quiz mechanics.
- **Persistent Storage:** Uses a file-based system (`highscore.txt`) to save and load player records.
- **Dynamic Questioning:** Integrated quiz logic that pairs arcade movement with educational content.
- **Responsive Controls:** Standard arrow key or WASD navigation.

## 📂 Project Structure
- `app.py`: The core game engine containing the Snake logic and Quiz interface.
- `highscore.txt`: Data file used to store the all-time high score.

## 🚀 Getting Started
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/snake-quiz-game.git](https://github.com/your-username/snake-quiz-game.git)
