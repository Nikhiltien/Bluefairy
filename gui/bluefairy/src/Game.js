// import { useState, useMemo, useCallback, useEffect } from "react";
// import { Chessboard } from "react-chessboard";
// import { Chess } from "chess.js";
// import CustomDialog from "./components/CustomDialog";

// function Game({ players, room, orientation, cleanup }) {
//   const chess = useMemo(() => new Chess(), []); // <- 1
//   const [fen, setFen] = useState(chess.fen()); // <- 2
//   const [over, setOver] = useState("");

//   // onDrop function
//   function onDrop() {} // <- 3
  
//   // Game component returned jsx
//   return (
//     <>
//       <div className="board">
//         <Chessboard position={fen} onPieceDrop={onDrop} />  {/**  <- 4 */}
//       </div>
//       <CustomDialog // <- 5
//         open={Boolean(over)}
//         title={over}
//         contentText={over}
//         handleContinue={() => {
//           setOver("");
//         }}
//       />
//     </>
//   );
// }

// export default Game;