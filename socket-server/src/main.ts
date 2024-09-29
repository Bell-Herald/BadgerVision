import { Server } from "socket.io";

const io = new Server(3000);
var C2 = null;

io.sockets.on("C2_AUTHORIZATION", function(socket) {
  C2 = socket.id;
});

io.on("connection", (socket) => {
  socket.onAny((eventName, ...args) => {
    console.log("Event", eventName, args);

    //Check that client2 (old server) has been initialized
    if(C2 == null) console.error("C2 not initialized")

    //If message is from client 2, send it to the target only (refrenced by socket id (sid))
    if(C2 != null && C2 == socket.id) {
      sid = args.sid;
      console.log("From C2 to", sid)
      socket.to(sid).emit(eventName, ...args);

    //If message is not from client 2, send it only to client2
    } else {
      if(C2 != null && C2 != socket.id) {
        socket.to(C2).emit(eventName, ...args);
      }
    }
  });
});