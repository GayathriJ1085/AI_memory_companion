type Message = {
  role: "user" | "assistant";
  content: string;
};

type MessageListProps = {
  messages: Message[];
};

export default function MessageList({
  messages,
}: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="flex flex-1 items-center justify-center px-6">
        <div className="text-center">
          <div className="mb-4 text-4xl">✦</div>

          <h2 className="text-2xl font-semibold">
            Hello!
          </h2>

          <p className="mt-2 text-zinc-500">
            Start a conversation with your AI companion.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-5 overflow-y-auto px-6 py-8">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${
            message.role === "user"
              ? "justify-end"
              : "justify-start"
          }`}
        >
          <div
            className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              message.role === "user"
                ? "bg-white text-black"
                : "bg-zinc-800 text-zinc-100"
            }`}
          >
            <p className="whitespace-pre-wrap text-sm leading-6">
              {message.content}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}