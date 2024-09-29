import { Server } from "socket.io";
import express from "express";
import http from "http";

// Create an Express application
const app = express();

// Create an HTTP server
const server = http.createServer(app);

// Attach the Socket.IO server to the HTTP server
const io = new Server(server);

// Add a health check endpoint
app.get("/health", (req, res) => {
  res.status(200).send("OK");
});

io.on("connection", (socket) => {
  socket.onAny((eventName, ...args) => {
    console.log("Event", eventName, args);
    socket.broadcast.emit(eventName, ...args);
  });
});

// Start the server
const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
