import { Component, For, Show } from "solid-js";
import { sendMessage } from "./../App";

let back_page_msg = { type: "game", method: "page_back", args: {} };

const BackButton: Component = () => {
  return (
    <button
      onclick={async () => {
        sendMessage(back_page_msg)
      }}
      class="btn"
    >

      Back
    </button>
  )
}

export default BackButton;
