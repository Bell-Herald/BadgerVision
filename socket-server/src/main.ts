import { Server } from "socket.io";

const io = new Server(3000);

io.on("connection", (socket) => {
  socket.onAny((eventName, ...args) => {
    console.log("Event", eventName, args);
    socket.broadcast.emit(eventName, ...args);
  });
});
