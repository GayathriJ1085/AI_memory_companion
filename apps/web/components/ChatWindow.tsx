"use client";

import { useState } from "react";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import LoadingIndicator from "./LoadingIndicator";
import { sendMessage as sendChatMessage } from "../lib/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [sessionId] = useState(
    () => `browser-${crypto.randomUUID()}`
  );

  const sendMessage = async (content: string) => {
    const userMessage: Message = {
      role: "user",
      content,
    };

    setMessages((previous) => [...previous, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const data = await sendChatMessage(sessionId, content);

      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (err) {
      console.error("Chat request failed:", err);

      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(
          "Unable to connect to the AI companion. Please try again."
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col bg-zinc-950 text-white">
      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="mx-auto flex max-w-4xl items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-zinc-800">
            ✦
          </div>

          <div>
            <h1 className="font-semibold">
              AI Memory Companion
            </h1>
            <p className="text-xs text-zinc-500">
              Online
            </p>
          </div>
        </div>
      </header>

      <div className="flex flex-1 flex-col">
        <div className="mx-auto flex w-full max-w-4xl flex-1 flex-col">
          <MessageList messages={messages} />

          {error && (
            <div className="mx-6 mb-4 rounded-xl border border-red-900 bg-red-950/40 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}

          {isLoading && <LoadingIndicator />}

          <MessageInput
            onSend={sendMessage}
            disabled={isLoading}
          />
        </div>
      </div>
    </main>
  );
}