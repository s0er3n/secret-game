import { Show, Component, createEffect, createSignal } from "solid-js";

import { sendMessage } from "./../App";
import { isHost } from "./Lobby";
import PlayerList from "./PlayerList";

let startGameMsg = { type: "game", method: "start", args: {} };

let setTimeMsg = {
  type: "game",
  method: "set_time",
  args: { time: 0 },
};

type Props = {
  time: number;
};

const SetTimePage = (props) => {
  return (
    <div class="flex justify-center">
      <h3>Settings:</h3>
      <p>start: {props.lobby().start_article}</p>
      <p>find: {props.lobby().articles_to_find.join(" | ")}</p>
      <span>max time: </span>
      <SetUserNameComponent time={props.lobby().time} />
      <span> seconds</span>
      <Show when={isHost(props)}>
        <p>
          <button
            class="btn"
            onclick={() => {
              sendMessage(startGameMsg);
            }}
          >
            start game
          </button>
        </p>
        <h3>How do I get Points?:</h3>
        <p>
          for every article you find you get 10 points and 5 extra points if you
          are the first person to find the article
        </p>
      </Show>
      <div>
        <h3>Players</h3>
        <PlayerList players={props.lobby()?.players} />
      </div>
    </div>
  );
};

const setTime = (e: any) => {
  let msg = setTimeMsg;
  msg.args.time = parseInt(e.target.value);
  sendMessage(msg);
};

const SetUserNameComponent: Component<Props> = (props) => {
  return (
    <input
      value={props.time}
      onchange={setTime}
      type="number"
      class="input input-bordered"
    />
  );
};

export default SetTimePage;
