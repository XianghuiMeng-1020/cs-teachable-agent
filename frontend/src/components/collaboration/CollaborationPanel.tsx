import { useState, useEffect, useRef } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { 
  Users, 
  MessageCircle, 
  Trophy, 
  Send,
  Crown,
  Zap,
  Lightbulb,
  HelpCircle,
  PartyPopper,
  LogIn,
  ArrowRight,
  User
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";
import { formatRelative } from "@/lib/utils";

interface CollaborationMessage {
  id: number;
  user_id: number;
  username: string;
  message_type: "chat" | "teaching_tip" | "question" | "celebration";
  content: string;
  created_at: string;
}

interface Participant {
  participant_id: number;
  user_id: number;
  username: string;
  contribution_score: number;
  progress: {
    learned_count: number;
    total_count: number;
    percentage: number;
  };
  gamification?: {
    points: number;
    level: number;
  };
}

interface CollaborationPanelProps {
  roomId?: number;
  domainId: string;
  currentUserId?: number;
}

const MESSAGE_TYPE_STYLES = {
  chat: { icon: MessageCircle, bg: "bg-slate-100", text: "text-slate-700" },
  teaching_tip: { icon: Lightbulb, bg: "bg-amber-100", text: "text-amber-700" },
  question: { icon: HelpCircle, bg: "bg-brand-100", text: "text-brand-700" },
  celebration: { icon: PartyPopper, bg: "bg-emerald-100", text: "text-emerald-700" },
};

export function CollaborationPanel({ roomId, domainId, currentUserId }: CollaborationPanelProps) {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState("chat");
  const [messageInput, setMessageInput] = useState("");
  const [selectedRoomId, setSelectedRoomId] = useState<number | null>(roomId || null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [lastMessageTime, setLastMessageTime] = useState<string | null>(null);

  // Join room mutation
  const joinRoomMutation = useMutation({
    mutationFn: async () => {
      const res = await apiFetch(`/collaboration/join?domain_id=${domainId}`, { method: "POST" });
      return res.json();
    },
    onSuccess: (data) => {
      setSelectedRoomId(data.room_id);
      queryClient.invalidateQueries({ queryKey: ["collaboration", "rooms"] });
    },
  });

  // Get room participants
  const { data: participantsData } = useQuery({
    queryKey: ["collaboration", "room", selectedRoomId, "participants"],
    queryFn: async () => {
      if (!selectedRoomId) return null;
      const res = await apiFetch(`/collaboration/room/${selectedRoomId}/participants`);
      return res.json();
    },
    enabled: !!selectedRoomId,
    refetchInterval: 10000, // Refresh every 10 seconds
  });

  // Get messages
  const { data: messagesData } = useQuery({
    queryKey: ["collaboration", "room", selectedRoomId, "messages"],
    queryFn: async () => {
      if (!selectedRoomId) return null;
      const res = await apiFetch(`/collaboration/room/${selectedRoomId}/messages?limit=50${lastMessageTime ? `&since=${lastMessageTime}` : ""}`);
      return res.json();
    },
    enabled: !!selectedRoomId,
    refetchInterval: 3000, // Refresh every 3 seconds for "real-time" feel
  });

  // Get leaderboard
  const { data: leaderboardData } = useQuery({
    queryKey: ["collaboration", "leaderboard", domainId],
    queryFn: async () => {
      const res = await apiFetch(`/collaboration/leaderboard?domain_id=${domainId}&limit=10`);
      return res.json();
    },
    enabled: activeTab === "leaderboard",
  });

  // Post message mutation
  const postMessageMutation = useMutation({
    mutationFn: async ({ message, type }: { message: string; type: string }) => {
      if (!selectedRoomId) throw new Error("No room selected");
      const res = await apiFetch(`/collaboration/room/${selectedRoomId}/message?message=${encodeURIComponent(message)}&message_type=${type}`, {
        method: "POST",
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["collaboration", "room", selectedRoomId, "messages"] });
      setMessageInput("");
    },
  });

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messagesData?.messages]);

  // Update last message time
  useEffect(() => {
    if (messagesData?.messages?.length > 0) {
      const lastMsg = messagesData.messages[messagesData.messages.length - 1];
      setLastMessageTime(lastMsg.created_at);
    }
  }, [messagesData?.messages]);

  const handleSendMessage = (type: string = "chat") => {
    if (!messageInput.trim()) return;
    postMessageMutation.mutate({ message: messageInput, type });
  };

  const participants = participantsData?.participants || [];
  const messages = messagesData?.messages || [];
  const sortedParticipants = [...participants].sort((a, b) => b.contribution_score - a.contribution_score);

  // Not joined yet
  if (!selectedRoomId) {
    return (
      <Card padding="lg" className="text-center">
        <div className="w-16 h-16 bg-brand-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Users className="w-8 h-8 text-brand-600" />
        </div>
        <h3 className="text-lg font-semibold text-slate-900">Collaborative Learning</h3>
        <p className="text-slate-500 mt-2 max-w-sm mx-auto">
          Join a study group to learn together with other students. Share tips, ask questions, and track your progress!
        </p>
        <Button
          className="mt-4"
          variant="primary"
          icon={LogIn}
          loading={joinRoomMutation.isPending}
          onClick={() => joinRoomMutation.mutate()}
        >
          Join Study Group
        </Button>
      </Card>
    );
  }

  return (
    <Card padding="none" className="overflow-hidden">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <div className="border-b border-slate-200 px-4 py-3">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5 text-brand-600" />
              <h3 className="font-semibold text-slate-900">
                {participantsData?.room_name || "Study Group"}
              </h3>
              <span className="text-xs text-slate-500">
                ({participants.length} online)
              </span>
            </div>
          </div>
          
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="chat">Chat</TabsTrigger>
            <TabsTrigger value="participants">Members</TabsTrigger>
            <TabsTrigger value="leaderboard">Rank</TabsTrigger>
          </TabsList>
        </div>

        {/* Chat Tab */}
        <TabsContent value="chat" className="m-0">
          <div className="h-[300px] overflow-y-auto p-4 space-y-3">
            {messages.length === 0 ? (
              <p className="text-center text-slate-400 text-sm py-8">
                No messages yet. Be the first to say hello!
              </p>
            ) : (
              messages.map((msg) => {
                const style = MESSAGE_TYPE_STYLES[msg.message_type] || MESSAGE_TYPE_STYLES.chat;
                const Icon = style.icon;
                const isMe = msg.user_id === currentUserId;
                
                return (
                  <div
                    key={msg.id}
                    className={cn(
                      "flex gap-2",
                      isMe && "flex-row-reverse"
                    )}
                  >
                    <div className={cn(
                      "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                      style.bg
                    )}>
                      <Icon className={cn("w-4 h-4", style.text)} />
                    </div>
                    <div className={cn(
                      "max-w-[80%]",
                      isMe && "text-right"
                    )}>
                      <div className="flex items-center gap-2 mb-0.5">
                        <span className="text-xs font-medium text-slate-700">
                          {msg.username}
                        </span>
                        <span className="text-[10px] text-slate-400">
                          {formatRelative(msg.created_at)}
                        </span>
                      </div>
                      <div className={cn(
                        "inline-block px-3 py-1.5 rounded-lg text-sm",
                        isMe ? "bg-brand-500 text-white" : "bg-slate-100 text-slate-700"
                      )}>
                        {msg.content}
                      </div>
                    </div>
                  </div>
                );
              })
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-slate-200 p-3">
            <div className="flex gap-2">
              <Input
                placeholder="Type a message..."
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                className="flex-1"
              />
              <Button
                icon={Send}
                onClick={() => handleSendMessage()}
                disabled={!messageInput.trim() || postMessageMutation.isPending}
              />
            </div>
            <div className="flex gap-2 mt-2">
              <button
                onClick={() => handleSendMessage("teaching_tip")}
                disabled={!messageInput.trim()}
                className="text-xs flex items-center gap-1 px-2 py-1 rounded bg-amber-50 text-amber-700 hover:bg-amber-100 disabled:opacity-50"
              >
                <Lightbulb className="w-3 h-3" /> Teaching Tip (+5 pts)
              </button>
              <button
                onClick={() => handleSendMessage("celebration")}
                disabled={!messageInput.trim()}
                className="text-xs flex items-center gap-1 px-2 py-1 rounded bg-emerald-50 text-emerald-700 hover:bg-emerald-100 disabled:opacity-50"
              >
                <PartyPopper className="w-3 h-3" /> Celebrate (+2 pts)
              </button>
            </div>
          </div>
        </TabsContent>

        {/* Participants Tab */}
        <TabsContent value="participants" className="m-0">
          <div className="p-4 space-y-3 max-h-[380px] overflow-y-auto">
            {sortedParticipants.map((p, index) => (
              <div
                key={p.participant_id}
                className="flex items-center gap-3 p-3 rounded-lg bg-slate-50"
              >
                <div className="relative">
                  <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-slate-500" />
                  </div>
                  {index === 0 && (
                    <div className="absolute -top-1 -right-1 w-5 h-5 bg-amber-400 rounded-full flex items-center justify-center">
                      <Crown className="w-3 h-3 text-amber-900" />
                    </div>
                  )}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-slate-900 truncate">
                      {p.username}
                    </span>
                    {p.user_id === currentUserId && (
                      <span className="text-[10px] bg-brand-100 text-brand-700 px-1.5 py-0.5 rounded">
                        You
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 text-xs text-slate-500 mt-0.5">
                    <span>Lv.{p.gamification?.level || 1}</span>
                    <span>•</span>
                    <span>{p.progress.percentage}% learned</span>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="flex items-center gap-1 text-brand-600">
                    <Zap className="w-4 h-4" />
                    <span className="font-semibold">{p.contribution_score}</span>
                  </div>
                  <span className="text-[10px] text-slate-400">
                    #{index + 1}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>

        {/* Leaderboard Tab */}
        <TabsContent value="leaderboard" className="m-0">
          <div className="p-4 max-h-[380px] overflow-y-auto">
            {leaderboardData?.leaderboard?.map((user: {
              rank: number;
              username: string;
              contribution_score: number;
              rooms_joined: number;
              level: number;
            }) => (
              <div
                key={user.rank}
                className={cn(
                  "flex items-center gap-3 p-3 rounded-lg mb-2",
                  user.rank <= 3 ? "bg-amber-50" : "bg-slate-50"
                )}
              >
                <div className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm",
                  user.rank === 1 ? "bg-amber-400 text-amber-900" :
                  user.rank === 2 ? "bg-slate-300 text-slate-700" :
                  user.rank === 3 ? "bg-orange-300 text-orange-900" :
                  "bg-slate-200 text-slate-600"
                )}>
                  {user.rank}
                </div>
                
                <div className="flex-1">
                  <span className="font-medium text-slate-900">{user.username}</span>
                  <div className="text-xs text-slate-500">
                    Lv.{user.level} • {user.rooms_joined} rooms
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="flex items-center gap-1 text-brand-600">
                    <Trophy className="w-4 h-4" />
                    <span className="font-semibold">{user.contribution_score}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
}
