<template>
  <div >
    <div v-if="chatOpen" class="chatbox-container" ref="chatbox">
      <div class="container">
        <div style="background-color: black;"> <center> <img class="logoImage" src="./MAPlogo.png" style="background-color: black; width:150px; align-items: center; justify-content: center; padding-bottom: 8px;" alt=""> </center> </div>
        <button @click="reloadChatbot" class="reloadButton">
          <center><img src="https://cdn.icon-icons.com/icons2/2469/PNG/512/reload_update_refresh_icon_149400.png" style="width: 50px; justify-content: end;"></center>
        </button>
        <div class="messageBox mt-8">
          <template v-for="(message, index) in messages" :key="index">
            <div :class="message.from == 'user' ? 'messageFromUser' : 'messageFromChatGpt'">
              <div :class="message.from == 'user' ? 'userMessageWrapper' : 'chatGptMessageWrapper'">
                <div :class="message.from == 'user' ? 'userMessageContent' : 'chatGptMessageContent'">{{ message.data }}</div>
              </div>
            </div>
          </template> 
        </div>
        <div class="inputContainer">
          <input
            v-model="currentMessage"
            type="text"
            class="messageInput"
            placeholder="Quelle est votre question ?"
            @keydown.enter="currentMessage && sendMessage(currentMessage);"
          />
          <button
            @click="currentMessage && sendMessage(currentMessage);"
            class="askButton"
          >
            ENVOYER
          </button>
        
        </div>
      </div>
    </div>
    <!-- Close / Open Chatbot -->
    <button @click="toggleChat" class="closeButton" style="position: fixed; bottom: 20px; right: 20px;">
      <img v-if="chatOpen" src="https://cdn-icons-png.flaticon.com/512/1380/1380370.png" alt="ChatOpen" style="width: 50px;">
      <img v-else src="https://cdn-icons-png.flaticon.com/512/1380/1380370.png" alt="ChatClosed" style="width: 50px;">
    </button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'ChatBox',
  data() {
    return {
      currentMessage: '',
      isLoading: false,
      messages: [],
      answers: [],
      chatOpen: true,
    };
  },
  methods: {
    // ... existing methods ...

    // Method to initialize the chatbox with a welcome message
    initializeChatbox() {
      this.messages.push({
        from: 'chatGpt',
        data: 'Je suis un chatbot dédié à la MAP. Posez vos questions, j\'y répondrai !',
      });
    },
    toggleChat() { 
      this.chatOpen = !this.chatOpen;
    },

    sendMessage(message) {
      axios.get('https://chatbotmap-7cabf-default-rtdb.firebaseio.com/interaction.json')
        .then(response => {
          const interactionData = response.data[0];
          interactionData.question = message;
          return axios.put('https://chatbotmap-7cabf-default-rtdb.firebaseio.com/interaction/0.json', interactionData);
        })
        .then(() => {
          console.log("Value updated successfully!");

          this.messages.push({
            from: 'user',
            data: message,
          });

          // Clear the message input after sending the user's message
          this.currentMessage = '';

          // Now we call the Python server to get the response
          // Display the "Waiting ..." message
          this.messages.push({
            from: 'chatGpt',
            data: "Attendez ",
          });

          // Scroll to the bottom after adding the new message
          this.$nextTick(() => {
            const messageBox = this.$el.querySelector('.messageBox');
            if (messageBox) {
              messageBox.scrollTo({
                top: messageBox.scrollHeight,
                behavior: 'smooth'
              });
            }
          });

          // Function to update the "Waiting ..." message with moving dots
          function updateWaitingMessage() {
            const lastMessage = this.messages[this.messages.length - 1];

            // Make sure the last message is from 'chatGpt' and contains "Waiting ..."
            if (lastMessage && lastMessage.from === 'chatGpt' && lastMessage.data.includes("Attendez")) {
              
              // Count the number of dots in the message
              const dotsCount = (lastMessage.data.match(/\./g) || []).length;
              const maxDots = 3; // Maximum number of dots to show

              // Remove the current "Waiting ..." message
              this.messages.pop();

              // Create a new "Waiting ..." message with one more dot
              const newDotsCount = (dotsCount + 1) % (maxDots + 1);
              const newDots = ".".repeat(newDotsCount);
              this.messages.push({
                from: 'chatGpt',
                data: `Attendez ${newDots}`,
              });

              // Scroll to the bottom after adding the new message
              this.$nextTick(() => {
                const messageBox = this.$el.querySelector('.messageBox');
                if (messageBox) {
                  messageBox.scrollTo({
                    top: messageBox.scrollHeight,
                    behavior: 'smooth'
                  });
                }
              });

            }
          }

          // Update the "Waiting ..." message every 500 milliseconds
          setInterval(updateWaitingMessage.bind(this), 500);

          fetch('http://127.0.0.1:5000/run', {
            method: 'GET'
          })
            .then(response => response.text())
            .then(data => {
            // Remove the "Waiting ..." message from messages array
            const waitingMessageIndex = this.messages.findIndex(message => message.data.includes("Attendez"));
            if (waitingMessageIndex !== -1) {
              this.messages.splice(waitingMessageIndex, 1);
            }

              this.$myGlobalVariable = data;
              const answers = { data: { data: this.$myGlobalVariable } };
              this.messages.push({
                from: 'chatGpt',
                data: answers.data.data,
              });

              // Scroll to the bottom after adding the new message
              this.$nextTick(() => {
                const messageBox = this.$el.querySelector('.messageBox');
                if (messageBox) {
                  messageBox.scrollTo({
                    top: messageBox.scrollHeight,
                    behavior: 'smooth'
                  });
                }
              });
            })
            .catch(error => console.error("Error:", error));

        })
        .catch(error => {
          console.error("Error:", error);
        });
    },
    reloadChatbot() {
      // Clear the chat history and reset chatbot state
      this.messages = [];

      // Add a welcome message to the messages array
      this.messages.push({
        from: 'chatGpt',
        data: 'Je suis un chatbot dédié à la MAP. Posez vos questions, j\'y répondrai !',
      });

      // Scroll to the bottom after adding the welcome message
      this.$nextTick(() => {
        const messageBox = this.$el.querySelector('.messageBox');
        if (messageBox) {
          messageBox.scrollTo({
            top: messageBox.scrollHeight,
            behavior: 'smooth'
          });
        }
      });
    },
  },
  mounted() {
    this.initializeChatbox();
  },
};
</script>



<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap');

*{
  font-family: 'Josefin Sans', sans-serif;
}

.closeButton {
  background-color: transparent;
  border: none;
}

/* Style for the Waiting message */
.waitingMessage {
  color: red;
}

.reloadButton {
  background-color: transparent;
  border: none;
}

.chatbox-container {
  position: fixed;
  bottom: 90px;
  right: 24px;
  z-index: 1000;
}

.container {
  background-color: #ecf6ff;
  border: solid 3px black;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Roboto', sans-serif;
}

/* Default styles for larger screens */
.container {
  width: 400px;
  height: 550px;
}

/* Media query for smaller screens (e.g., mobile devices) */
@media only screen and (max-width: 767px) {
  .container {
    width: 90vw; 
    height: 88vh; 
    max-width: 90vw; 
    max-height: 88vh;
  }
}

h1 {
  font-size: 24px;
  font-weight: 500;
  text-align: center;
  color: white;
  padding: 16px;
  margin: 0;
  background-color: black;
  border-bottom: 1px solid #e7e7e7;
}
.logoImage {
  margin: 0;
  background-color: black;
}

.messageBox {
  padding-bottom: 16px;
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

@media (max-width: 767px) {
  .messageBox{
    padding-bottom: 200px;
  }
  .userMessageContent,
  .chatGptMessageContent {
    max-width: 14rem !important;
    font-size: 22px !important;
  }
}

.messageFromUser,
.messageFromChatGpt {
  display: flex; }

.messageFromUser,
.messageFromChatGpt {
  display: flex;
  margin-bottom: 8px;
}

.userMessageWrapper,
.chatGptMessageWrapper {
  display: flex;
  flex-direction: column;
}

.userMessageWrapper {
  align-self: flex-end;
}

.chatGptMessageWrapper {
  align-self: flex-start;
}

.userMessageContent,
.chatGptMessageContent {
  max-width: 6rem;
  padding: 8px 12px;
  border-radius: 18px;
  margin-bottom: 2px;
  font-size: 16px;
  line-height: 1.4;
  overflow-wrap: break-word;
}

.userMessageContent {
  background-color: #e0e0e0;
  color: black;
  border: solid 2px black;
  border-top-left-radius: 0;
  margin-right: 15px;
}

.chatGptMessageContent {
  background-color: #1E7BCA;
  color: white;
  border: solid 2px black;
  border-top-right-radius: 0;
  margin-left: 15px;
}

.userMessageTimestamp,
.chatGptMessageTimestamp {
  font-size: 10px;
  color: #999;
  margin-top: 2px;
}

.userMessageTimestamp {
  align-self: flex-end;
}

.chatGptMessageTimestamp {
  align-self: flex-start;
}

.inputContainer {
  display: flex;
  align-items: center;
  background-color: white;
  padding: 8px 8px 8px 8px;
  margin: 8px 8px 8px 8px;
  border: solid 3px black;  
}

.messageInput {
  flex-grow: 1;
  border: none;
  outline: none;
  font-size: 16px;
  background-color: white;
  margin-right: 10px;
}

.askButton {
  background-color: black;
  color: white;
  font-size: 16px;
  padding: 14px 10px;
  border: none;
  outline: none;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

@media (max-width: 480px) {
  .container {
    width: 100%;
    max-width: none;
    border-radius: 0;
  }
}




.messageFromChatGpt {
  display: flex;
}

.messageFromUser {
  display: flex;
  justify-content: flex-end;
}
</style>
