import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-zinc-950 px-6 text-white">
      <div className="w-full max-w-2xl text-center">
        <div className="mb-6 text-5xl">✦</div>

        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
          AI Memory Companion
        </h1>

        <p className="mx-auto mt-4 max-w-lg text-zinc-400">
          A friendly AI companion designed to have natural, meaningful
          conversations.
        </p>

        <Link
          href="/chat"
          className="mt-8 inline-flex rounded-xl bg-white px-6 py-3
                     font-medium text-black transition hover:bg-zinc-200"
        >
          Start Conversation
        </Link>
      </div>
    </main>
  );
}