import { useState, FormEvent } from 'react';
import './App.css';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  status: 'pending_video_generation' | 'video_ready' | 'text_only' | 'error';
  videoUrl?: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [courseId, setCourseId] = useState<string>('course-123'); // Default course ID for MVP
  const [token, setToken] = useState<string>('dummy-token'); // Dummy token for MVP

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: input,
      status: 'text_only', // User messages are always text_only
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');

    try {
      const response = await fetch(`http://localhost:3000/courses/${courseId}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ question: userMessage.text }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: `ai-error-${Date.now()}`,
            sender: 'ai',
            text: `Error: ${errorData.message || response.statusText}`,
            status: 'error',
          },
        ]);
        return;
      }

      const data = await response.json();
      const aiInterimMessage: Message = {
        id: data.messageId,
        sender: 'ai',
        text: data.interimText,
        status: data.status,
      };
      setMessages((prevMessages) => [...prevMessages, aiInterimMessage]);
    } catch (error: any) {
      console.error('Failed to send message:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: `ai-network-error-${Date.now()}`,
          sender: 'ai',
          text: `Network error: ${error.message}`,
          status: 'error',
        },
      ]);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Avatar Course Chat</h1>
      </header>
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.sender}`}>
              <p>{msg.text}</p>
              {/* Video display logic will go here in the next step */}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="message-input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your course question..."
          />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default App;