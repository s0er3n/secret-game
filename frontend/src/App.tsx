import { For, Component, createEffect, Show } from "solid-js";
import { createSignal } from "solid-js";

import Header from "./lobby/Header";
import JoinOrCreateLobby from "./JoinOrCreateLobby";
import SetUserName from "./SetUserName";
import Lobby, { setGoToLobby } from "./lobby/Lobby";
import { TLobby, TWiki } from "./types";

let [connected, setConnection] = createSignal<boolean>(false);
let [hasUserName, setHasUserName] = createSignal<boolean>(false);
let ws: WebSocket | null = null;

export function sendMessage(msg: any) {
  if (ws) {
    ws.send(JSON.stringify(msg));
  } else {
    console.warn("websocket not connected");
  }
}

// let [players, setPlayers = createSignal([])

let [wiki, setWiki] = createSignal<TWiki>();
let id = localStorage.getItem("id");

let setUserNameMsg = {
  type: "player",
  method: "set_user_name",
  args: { name: "Gast" },
};

if (!id) {
  id = self.crypto.randomUUID();
  localStorage.setItem("id", id);
}

const [search, setSearch] = createSignal([]);

export const startWS = () => {
  ws = new WebSocket(`${import.meta.env.VITE_backend_url}/ws/${id}`);

  ws.onopen = (_) => {
    setConnection(true);
    let username = localStorage.getItem("username");
    if (username) {
      let msg = setUserNameMsg;
      setUserNameMsg.args.name = username;
      sendMessage(msg);
      setHasUserName(true);
    }
    // joining lobby if you were in a lobby before
    const urlSearchParams = new URLSearchParams(window.location.search);
    if (urlSearchParams.get("code")) {
      let joinLobbyMsg = {
        type: "lobby",
        method: "join_lobby",
        args: { id: urlSearchParams.get("code") },
      };
      sendMessage(joinLobbyMsg);
    }
  };

  ws.onclose = () => {
    setLobby(null);
    setConnection(false);
  };
  ws.onmessage = (e) => {
    let data = JSON.parse(e.data);
    if (data.method === "LobbyUpdate") {
      const urlParams = new URLSearchParams(window.location.search);
      urlParams.set("code", data.id);
      window.history.pushState(null, "", "?" + urlParams.toString());

      console.log(data);
      if (data?.state == "over") {
        setGoToLobby(false);
      }
      setLobby(data);
    } else if (data.method === "Wiki" && !Array.isArray(data.data)) {
      setWiki(data.data);
      window.scrollTo(0, 0);
      console.log(data);
      // search -> maybe add a method on backend
    } else if (typeof data.data === "object") {
      console.log(data.data);
      if (!data.data.error) {
        setSearch(data.data);
      }
    } else {
      console.log(e);
    }
  };
};

let [lobby, setLobby] = createSignal<TLobby | null>(null);

if (localStorage.getItem("username")) {
  startWS();
}

const App: Component = () => {
  // derived state if player is host

  return (
    <div>
      <Header lobby={lobby} id={id} />

      <Show when={!hasUserName()}>
        <SetUserName setHasUserName={setHasUserName} />
      </Show>
      <Show when={hasUserName()}>
        <div>
          <Show
            when={connected()}
            fallback={
              <button
                class="w-96"
                onclick={() => {
                  startWS();
                }}
              >
                start ws connection
              </button>
            }
          >
            <Show when={lobby()}>
              <Lobby wiki={wiki} id={id} lobby={lobby} search={search} />
            </Show>
            <Show when={!lobby() && hasUserName()}>
              <JoinOrCreateLobby />
            </Show>
          </Show>
        </div>
      </Show>
    </div>
  );
};

export default App;
