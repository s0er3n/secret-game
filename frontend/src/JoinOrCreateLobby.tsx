import { Component, createEffect, createSignal } from "solid-js";

import { sendMessage } from "./App";
let [idToJoin, setIdToJoin] = createSignal<string>("");

let joinLobbyMsg = {
  type: "lobby",
  method: "join_lobby",
  args: { id: idToJoin() },
};

createEffect(() => {
  joinLobbyMsg = {
    type: "lobby",
    method: "join_lobby",
    args: { id: idToJoin() },
  };
});

let newLobbyMsg = { type: "lobby", method: "new_lobby", args: {} };

const JoinOrCreateLobby: Component = () => {
  return (
    <div>
      <input
        onchange={(e) => setIdToJoin(e.target.value)}
        type="text"
        placeholder="type in the code…"
        class="input input-bordered"
      />
      <button
        class="btn "
        onclick={() => {
          sendMessage(joinLobbyMsg);
        }}
      >
        join lobby
      </button>
      <button
        class="btn"
        onclick={() => {
          sendMessage(newLobbyMsg);
        }}
      >
        create a new lobby
      </button>
    </div>
  );
};

export default JoinOrCreateLobby;
