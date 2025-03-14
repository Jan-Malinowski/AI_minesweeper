🧠 Minesweeper AI – Reinforcement Learning with Q-Learning<br>

🎯 Project Overview<br>

This project is an AI-powered Minesweeper player built using Python, Pygame, and Q-learning. It utilizes reinforcement learning (RL) to improve its decision-making over time. Initially, the AI makes random moves, but as it trains, it starts learning the best moves using a reward-based system.<br>
 
The AI aims to minimize the number of incorrect moves while maximizing successful reveals, gradually learning how to play Minesweeper intelligently without prior knowledge of the game’s rules.<br>

🚀 Features<br>
✅ Pygame-based Minesweeper – A custom-built game grid with interactive gameplay.<br>
✅ Reinforcement Learning – The AI uses Q-learning to optimize its moves.<br>
✅ Reward System – AI gets positive rewards for safe moves and penalties for hitting mines.<br>
✅ Exploration vs. Exploitation – The AI balances learning new moves with using learned knowledge.<br>
✅ Auto-restart & Training Mode – The AI continuously plays, improving with each game.<br>

🏗️ How It Works<br>
Game Environment –&emsp;A standard Minesweeper grid is created using Pygame.<br>
AI Decision Making –&emsp;The AI selects moves randomly at first, then refines its choices using Q-learning.<br>
Rewards & Punishments:<br>
&emsp;✅ +10 for revealing a safe cell<br>
&emsp;✅ +50 for correctly flagging a mine<br>
&emsp;❌ -100 for clicking on a mine (losing the game)<br>
Q-Table Updates – The AI updates its Q-table after every move using:<br>
 &emsp;Q(s,a)=Q(s,a)+α×(r+γ×maxQ(s′, a′)−Q(s,a))<br>
 &emsp;where α is the learning rate, γ is the discount factor, and r is the reward.<br>
Learning Over Time –&emsp;The AI starts exploring the grid but gradually learns optimal moves by adjusting the exploration rate (ε).<br>
<br>
🏆First victory after 51000 attempts<br><br>
<img width="604" alt="Screenshot 2025-03-14 at 19 23 53" src="https://github.com/user-attachments/assets/77429278-b1bf-42e7-9d12-cced75ad7174" />
