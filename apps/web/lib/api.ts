const API_BASE_URL = "http://127.0.0.1:8000";

export interface ChatResponse {
  session_id: string;
  response: string;
  model: string;
}

export async function sendMessage(
  sessionId: string,
  message: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      message,
    }),
  });

  if (!response.ok) {
    let errorMessage = "Failed to communicate with the AI.";

    try {
      const errorData = await response.json();

      if (typeof errorData?.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}