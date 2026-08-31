export default function LoadingIndicator() {
  return (
    <div className="px-6 pb-3">
      <div className="flex items-center gap-2 text-sm text-zinc-500">
        <span>Companion is thinking</span>

        <span className="flex gap-1">
          <span className="animate-bounce">.</span>
          <span className="animate-bounce [animation-delay:150ms]">.</span>
          <span className="animate-bounce [animation-delay:300ms]">.</span>
        </span>
      </div>
    </div>
  );
}