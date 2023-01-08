import { createSignal, onCleanup } from "solid-js";

const timeBetweenDates = (validTill: number) => {
  const validFromDate = new Date();
  const validTillDate = new Date(validTill);
  const difference = validTillDate.getTime() - validFromDate.getTime();

  let timeData = {
    minutes: "00",
    seconds: "00",
  };

  if (difference > 0) {
    let seconds = Math.floor(difference / 1000);
    let minutes = Math.floor(seconds / 60);

    minutes %= 60;
    seconds %= 60;

    timeData = {
      minutes: minutes < 10 ? `0${minutes}` : `${minutes}`,
      seconds: seconds < 10 ? `0${seconds}` : `${seconds}`,
    };
  }
  return {
    timeData,
    difference,
  };
};

interface Props {
  validTill: number;
}

const Ticker = ({ validTill }: Props) => {
  const [timerDetails, setTimerDetails] = createSignal(
    timeBetweenDates(validTill).timeData
  );
  const timer = setInterval(() => {
    setTimerDetails(timeBetweenDates(validTill).timeData);
  }, 1000);

  onCleanup(() => clearInterval(timer));

  return (
    <>
      <span>{timerDetails().minutes}</span>m
      <span>{timerDetails().seconds}</span>s
    </>
  );
};

export default Ticker;
