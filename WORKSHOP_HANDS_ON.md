# 🎓 Hands-On Workshop: Exploring "The Wall of Whispering Frames"
## Learn by Doing - Small Tasks Edition

**Duration:** 2-3 hours  
**Approach:** Clone → Explore → Modify → Understand

---

## 🎯 **Workshop Philosophy**

Instead of building from scratch, we'll:
1. **Clone** the working project
2. **Explore** how it works
3. **Modify** small parts to understand
4. **Experiment** with changes
5. **Learn** by doing!

---

## 📋 **Part 1: Setup & Clone** (15 minutes)

### Task 1.1: Clone the Repository
```bash
# Clone the project
git clone [YOUR_GITHUB_URL]
cd Portrait

# See what we have
ls -la
```

**What to explain:**
- "This is a working project - we're going to explore it!"
- Show the folder structure
- Explain what each folder does

### Task 1.2: Install Dependencies
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install -r backend/requirements.txt

# Install Node packages
cd frontend
npm install
cd ..
```

**What to explain:**
- "These are the tools our project needs"
- Show what each package does (briefly)
- "Think of it like installing apps on your phone"

### Task 1.3: Get API Key
```bash
# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

**What to explain:**
- "This key lets our portraits be smart"
- Show them how to get one (if needed)
- "Without it, portraits use simple templates"

---

## 🎨 **Part 2: Explore the Frontend** (30 minutes)

### Task 2.1: Find the Main App
**Your Task:**
1. Open `frontend/src/App.jsx`
2. Find where the portraits are defined
3. Count how many portraits there are

**What to explain:**
- "This is the main page - it's like the control center"
- Show the PORTRAITS array
- "Each portrait has an ID, name, and images"

**Try This:**
- Change one portrait's name
- Refresh and see what happens!

### Task 2.2: Explore Portrait Component
**Your Task:**
1. Open `frontend/src/components/Portrait.jsx`
2. Find what makes a portrait "awake"
3. Find the speaking indicator (💬)

**What to explain:**
- "This component shows ONE portrait"
- "isAwake prop controls if it's sleeping or awake"
- "When awake, it glows and shows the 💬"

**Try This:**
- Change the emoji to something else (🎭, ✨, 🔮)
- See it appear when portraits speak!

### Task 2.3: Explore Portrait Gallery
**Your Task:**
1. Open `frontend/src/components/PortraitGallery.jsx`
2. Find where Fat Lady is separated
3. Find the square grid for other portraits

**What to explain:**
- "This arranges all portraits on the wall"
- "Fat Lady is special - she's tall!"
- "Others are in a 2x2 square grid"

**Try This:**
- Change the grid layout (swap positions)
- See how it affects the display!

### Task 2.4: Explore Camera Feed
**Your Task:**
1. Open `frontend/src/components/CameraFeed.jsx`
2. Find where it takes pictures (every 5 seconds)
3. Find where it sends images to the backend

**What to explain:**
- "This uses your webcam"
- "Takes a picture every 5 seconds"
- "Sends it to the backend to detect objects"

**Try This:**
- Change the interval from 5000 to 10000 (10 seconds)
- See how it affects detection speed!

---

## 🧠 **Part 3: Explore the Backend** (30 minutes)

### Task 3.1: Find the API Server
**Your Task:**
1. Open `backend/api/main.py`
2. Find the root endpoint (`@app.get("/")`)
3. Find where routes are included

**What to explain:**
- "This is the server - like a restaurant"
- "Endpoints are like menu items"
- "Routes are different services"

**Try This:**
- Change the welcome message
- Restart backend and see it change!

### Task 3.2: Explore Object Detection
**Your Task:**
1. Open `backend/api/routes/detection.py`
2. Find where YOLO detects objects
3. Find what confidence threshold is used

**What to explain:**
- "YOLO is like teaching a computer to see"
- "It looks at images and finds objects"
- "Confidence = how sure it is"

**Try This:**
- Change the confidence threshold (0.5 → 0.3)
- See if it detects more objects!

### Task 3.3: Explore Conversation Engine
**Your Task:**
1. Open `backend/models/conversation_engine.py`
2. Find where OpenAI is called
3. Find the personality descriptions

**What to explain:**
- "This makes portraits smart"
- "Each portrait has a personality"
- "AI uses personality to generate responses"

**Try This:**
- Change one portrait's personality
- See how their responses change!

### Task 3.4: Explore Portrait Data
**Your Task:**
1. Open `backend/data/portraits.json`
2. Read each portrait's personality
3. Find the voice settings

**What to explain:**
- "This is the portrait database"
- "Personality = how they act"
- "Voice = how they sound"

**Try This:**
- Change Fat Lady's personality to "funny and silly"
- Test it and see the difference!

---

## 🎨 **Part 4: Styling & Theme** (20 minutes)

### Task 4.1: Explore the Dark Theme
**Your Task:**
1. Open `frontend/src/App.css`
2. Find the background colors
3. Find the gold color (#d4af37)

**What to explain:**
- "This makes it look like Hogwarts"
- "Dark colors = mysterious corridor"
- "Gold = magical highlights"

**Try This:**
- Change gold to another color (purple, blue, green)
- See how it changes the feel!

### Task 4.2: Explore Portrait Styling
**Your Task:**
1. Open `frontend/src/components/Portrait.css`
2. Find the glow animation
3. Find the frame border style

**What to explain:**
- "CSS makes things look pretty"
- "Animations make it feel alive"
- "Borders make it look like frames"

**Try This:**
- Change the border color
- Change the glow color
- See the visual changes!

### Task 4.3: Explore Conversation Styling
**Your Task:**
1. Open `frontend/src/components/ConversationLog.css`
2. Find the message styling
3. Find the scrollbar styling

**What to explain:**
- "Messages look like parchment"
- "Custom scrollbars match theme"
- "Hover effects add interactivity"

**Try This:**
- Change message background color
- Change the border color
- Make it your own!

---

## 🔧 **Part 5: Hands-On Modifications** (40 minutes)

### Task 5.1: Add Your Own Portrait
**Your Task:**
1. Take a photo of yourself (or use a picture)
2. Save it as `yourname-sleep.png` and `yourname-awake.png`
3. Add to `frontend/public/portraits/`
4. Add to `frontend/src/App.jsx` PORTRAITS array
5. Add personality to `backend/data/portraits.json`

**What to explain:**
- "You can add yourself as a portrait!"
- "Need both sleep and awake images"
- "Personality affects what you say"

**Show them:**
- How to add to the array
- How to add personality
- Test it together!

### Task 5.2: Change a Personality
**Your Task:**
1. Pick a portrait (e.g., Sir Cadogan)
2. Open `backend/data/portraits.json`
3. Change their personality description
4. Restart backend
5. Test with an object

**What to explain:**
- "Personality = how they act"
- "More dramatic = more dramatic responses"
- "Funny = funnier responses"

**Show them:**
- Before and after examples
- How personality affects conversations

### Task 5.3: Change Detection Speed
**Your Task:**
1. Open `frontend/src/components/CameraFeed.jsx`
2. Find the interval (5000 = 5 seconds)
3. Change it to 3000 (3 seconds) or 10000 (10 seconds)
4. See how it affects detection

**What to explain:**
- "Faster = more detections, but uses more resources"
- "Slower = less detections, but smoother"
- "Find the right balance"

**Show them:**
- Test different speeds
- Discuss trade-offs

### Task 5.4: Change Conversation Length
**Your Task:**
1. Open `backend/models/conversation_engine.py`
2. Find where it generates 4 turns
3. Change to 3 or 5 turns
4. Test the difference

**What to explain:**
- "More turns = longer conversations"
- "Fewer turns = quicker responses"
- "Balance between interesting and not too long"

**Show them:**
- Test with 3, 4, and 5 turns
- See which feels best

### Task 5.5: Customize Colors
**Your Task:**
1. Pick a color scheme (e.g., purple theme, blue theme)
2. Change colors in CSS files
3. See the transformation

**What to explain:**
- "Colors set the mood"
- "Dark = mysterious, Bright = cheerful"
- "Match colors to your theme"

**Show them:**
- Before and after
- How colors affect feel

---

## 🎮 **Part 6: Testing & Experimentation** (20 minutes)

### Task 6.1: Test Different Objects
**Your Task:**
1. Hold up different objects
2. See what conversations happen
3. Notice how portraits react differently

**What to explain:**
- "Different objects = different conversations"
- "Each portrait has unique reactions"
- "AI makes it interesting every time"

**Discussion:**
- "What surprised you?"
- "Which portrait is your favorite?"
- "What object got the best reaction?"

### Task 6.2: Test Without API Key
**Your Task:**
1. Temporarily rename `.env` to `.env.backup`
2. Restart backend
3. Test conversations
4. See the difference (templates vs AI)

**What to explain:**
- "Without API key = simple templates"
- "With API key = smart AI conversations"
- "This shows the power of AI!"

**Show them:**
- Side-by-side comparison
- Why AI makes it better

### Task 6.3: Experiment with Personalities
**Your Task:**
1. Make all portraits "funny"
2. Test conversations
3. Make all "serious"
4. Compare the difference

**What to explain:**
- "Personality affects everything"
- "Same object, different personalities = different responses"
- "This is how AI works with context"

---

## 🎓 **Part 7: Understanding Concepts** (15 minutes)

### Concept 1: How Object Detection Works
**Explain:**
- "YOLO is trained on millions of images"
- "It learned patterns (cup = round, handle, etc.)"
- "When it sees similar patterns, it recognizes them"

**Show:**
- Simple diagram of detection process
- Example: "This looks like a cup because..."

### Concept 2: How AI Conversations Work
**Explain:**
- "LLM (like ChatGPT) reads the object name"
- "It uses personality to generate response"
- "It considers previous conversation too"

**Show:**
- Example prompt to AI
- How personality affects output

### Concept 3: How Frontend & Backend Talk
**Explain:**
- "Frontend sends request (like ordering food)"
- "Backend processes it (like kitchen)"
- "Backend sends response (like food arrives)"

**Show:**
- Request/response flow
- Use restaurant analogy

### Concept 4: How Styling Works
**Explain:**
- "CSS is like decorating"
- "Colors, shadows, animations"
- "Makes it look magical"

**Show:**
- Before/after styling
- How CSS transforms appearance

---

## 🎯 **Part 8: Your Turn!** (20 minutes)

### Challenge Tasks (Pick 2-3)

**Challenge 1: Add Animation**
- Add a fade-in when portraits wake up
- Add a shake when they're excited
- Make it your own!

**Challenge 2: Change Layout**
- Make Fat Lady square and others tall
- Try a different grid arrangement
- Experiment!

**Challenge 3: Add Sound Effects**
- Add a "whoosh" when portraits wake
- Add background music
- Make it immersive!

**Challenge 4: Custom Theme**
- Create your own color scheme
- Add your own style
- Make it unique!

**Challenge 5: Add More Portraits**
- Add 2-3 more portraits
- Give them unique personalities
- Test conversations!

---

## 🎉 **Part 9: Share & Celebrate** (10 minutes)

### Show and Tell
- Each student shows one thing they changed
- Explain what they did
- Show the result

### Discussion
- "What did you learn?"
- "What surprised you?"
- "What would you add next?"

### Next Steps
- How to continue learning
- Resources to explore
- How to share your project

---

## 📝 **Quick Reference: File Locations**

### Frontend Files
- `frontend/src/App.jsx` - Main app
- `frontend/src/components/Portrait.jsx` - Single portrait
- `frontend/src/components/PortraitGallery.jsx` - All portraits
- `frontend/src/components/CameraFeed.jsx` - Camera
- `frontend/src/App.css` - Main styling
- `frontend/src/components/Portrait.css` - Portrait styling

### Backend Files
- `backend/api/main.py` - Server
- `backend/api/routes/detection.py` - Object detection
- `backend/api/routes/conversation.py` - Conversations
- `backend/models/conversation_engine.py` - AI brain
- `backend/data/portraits.json` - Portrait data

---

## 🎯 **Teaching Tips**

### For Each Task:
1. **Show them first** - Demonstrate the task
2. **Explain why** - What does this do?
3. **Let them try** - Hands-on practice
4. **Check understanding** - "What did you change?"
5. **Celebrate** - "Great job!"

### Keep It Fun:
- Use analogies they understand
- Celebrate small wins
- Encourage experimentation
- Make mistakes together
- Ask questions

### Pacing:
- Don't rush - better to understand than finish
- Take breaks every 45 minutes
- Check in: "Everyone good?"
- Adapt to the group

---

## 🎁 **Bonus: Extension Ideas**

If students finish early:
- Add more portraits
- Create custom themes
- Add sound effects
- Change animations
- Experiment with personalities
- Try different objects
- Share with friends

---

**Have fun exploring and learning! 🎓✨**

