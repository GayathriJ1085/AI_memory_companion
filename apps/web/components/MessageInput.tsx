"use client";

import { FormEvent, useState } from "react";

type MessageInputProps = {
  onSend: (message: string) => void;
  disabled?: boolean;
};

export default function MessageInput({
  onSend,
  disabled = false,
}: MessageInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

    onSend(trimmedMessage);
    setMessage("");
  };

  return (
    <div className="border-t border-zinc-800 px-6 py-4">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-4xl gap-3"
      >
        <input
          type="text"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Type a message..."
          disabled={disabled}
          className="flex-1 rounded-xl border border-zinc-700
                     bg-zinc-900 px-4 py-3 text-sm text-white
                     outline-none placeholder:text-zinc-500
                     focus:border-zinc-500 disabled:opacity-50"
        />

        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="rounded-xl bg-white px-5 py-3 text-sm
                     font-medium text-black transition
                     hover:bg-zinc-200 disabled:cursor-not-allowed
                     disabled:opacity-40"
        >
          Send
        </button>
      </form>
    </div>
  );
}