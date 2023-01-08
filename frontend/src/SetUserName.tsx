import { Component, createEffect, createSignal } from "solid-js";

import { sendMessage, startWS } from "./App";
let [userName, setUserName] = createSignal<string>(
  `Gast ${Math.floor(Math.random() * 1000)}`
);

let setUserNameMsg = {
  type: "player",
  method: "set_user_name",
  args: { name: userName() },
};

const SetUserNameComponent: Component<any> = (props) => {
  return (
    <div class="w-full flex flex-row items-center justify-center justify-items-center">
      <input
        value={userName()}
        onchange={(e) => setUserName(e.target.value)}
        type="text"
        class="input input-bordered"
      />
      <button
        class="btn "
        onclick={() => {
          if (userName().length > 3) {
            let msg = setUserNameMsg;
            setUserNameMsg.args.name = userName();
            sendMessage(msg);
            localStorage.setItem("username", userName());
            props.setHasUserName(true);
            startWS();
          } else {
            alert("user name should be longer than 3 chars");
          }
        }}
      >
        set username
      </button>
    </div>
  );
};

export default SetUserNameComponent;
