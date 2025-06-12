import streamlit as st
import time

class MiniGame:
    def __init__(self, duration=15):
        self.duration = duration
        self._initialize_state()

    def _initialize_state(self):
        for key, value in {
            "score": 0,
            "game_over": False,
            "start_time": None
        }.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def start_game(self):
        st.title("🎮 Mini Click Game")
        st.markdown(f"Click the 🎯 button as fast as you can in **{self.duration} seconds**!")

        # Game started?
        if st.session_state["start_time"] is None:
            if st.button("Start Game"):
                st.session_state["score"] = 0
                st.session_state["start_time"] = time.time()
                st.session_state["game_over"] = False
                st.rerun()  # 👈 force Streamlit to refresh state and enter next block

        elif not st.session_state["game_over"]:
            elapsed = time.time() - st.session_state["start_time"]

            if st.button("🎯 Click me!"):
                st.session_state["score"] += 1

            st.write(f"⏱ Time Left: **{round(self.duration - elapsed, 1)} seconds**")
            st.write(f"🏆 Score: **{st.session_state['score']}**")

            if elapsed >= self.duration:
                st.session_state["game_over"] = True
                st.rerun()

        elif st.session_state["game_over"]:
            st.success(f"⏳ Time's up! Your final score: **{st.session_state['score']}**")
            st.balloons()
            if st.button("Play Again"):
                st.session_state["start_time"] = None
                st.session_state["score"] = 0
                st.session_state["game_over"] = False
                st.rerun()
