import { VideoPlayer, VideoPlayerContainer } from "@zoom/videosdk";
import { DetailedHTMLProps, HTMLAttributes, RefObject } from "react";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      ["video-player"]: DetailedHTMLProps<
        HTMLAttributes<VideoPlayer>,
        VideoPlayer
      > & { class?: string };

      ["video-player-container"]: DetailedHTMLProps<
        HTMLAttributes<VideoPlayerContainer>,
        VideoPlayerContainer
      > & {
        class?: string;
        ref?: RefObject<HTMLDivElement>;
      };
    }
  }
}
