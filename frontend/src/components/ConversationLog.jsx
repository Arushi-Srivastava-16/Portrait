import React from 'react';
import './ConversationLog.css';

export default function ConversationLog({ conversation }) {
  return (
    <div className="conversation-log">
      <h2>Conversation History</h2>
      <div className="conversation-messages">
        {conversation.length === 0 ? (
          <p className="empty-message">No conversations yet. Show an object to the camera!</p>
        ) : (
          conversation.map((turn, index) => (
            <div key={index} className="conversation-turn">
              <div className="portrait-label">{turn.portrait}:</div>
              <div className="message-text">{turn.text}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

