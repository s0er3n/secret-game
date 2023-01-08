import { Component } from "solid-js";

const Article: Component<{ title: string; points?: number }> = (props) => {
  return (
    <>
      <b>{props.title}</b> {props.points ? "(" + props.points + ")" : ""}
    </>
  );
};

export default Article;
