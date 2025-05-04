import React, { useState, useRef, useEffect } from 'react';
import { Card, Form, Button } from 'react-bootstrap';

function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! How can I help you ?' }
  ]);
  const [userInput, setUserInput] = useState('');
  const chatEndRef = useRef(null);

  const handleSend = async () => {
    if (userInput.trim() === '') return;
  
    const newMessages = [...messages, { sender: 'user', text: userInput }];
    setMessages(newMessages);
    setUserInput('');
  
    const botResponse = await getBotResponse(userInput);
    setMessages([...newMessages, { sender: 'bot', text: botResponse }]);
  };
  const getBotResponse = async (input) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: input })
      });
  
      const data = await response.json();
      return data.reply;
    } catch (error) {
      console.error(error);
      return 'Erreur de communication avec le serveur.';
    }
  };

  // Scroll automatique en bas
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="d-flex flex-column vh-100 vw-100">
      <Card className="flex-grow-1 rounded-0 border-0">
        <Card.Header className="bg-primary text-white">
          <h4 className="m-0">Medif</h4>
        </Card.Header>
        <Card.Body className="overflow-auto d-flex flex-column">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`d-flex mb-2 ${
                msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'
              }`}
            >
              <div
                className={`p-2 rounded ${
                  msg.sender === 'user' ? 'bg-success text-white' : 'bg-light'
                }`}
                style={{ maxWidth: '75%' }}
              >
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </Card.Body>
        <Card.Footer className="bg-light">
          <Form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
          >
            <div className="d-flex">
              <Form.Control
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Écris un message..."
                className="me-2"
              />
              <Button variant="primary" type="submit">
                Envoyer
              </Button>
            </div>
          </Form>
        </Card.Footer>
      </Card>
    </div>
  );
}

export default Chatbot;
