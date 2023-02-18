PetiteVue.createApp({
  get subtitlesList() {
    return [
      {
        id: 1,
        start_time: 0,
        end_time: 10,
        title:
          "Lorem, ipsum dolor sit amet consectetur adipisicing elit. A, possimus Lorem, ipsum dolor sit amet consectetur adipisicing elit. A, possimus.",
      },
      {
        id: 2,
        start_time: 11,
        end_time: 14,
        title:
          "Lorem, ipsum dolor sit amet consectetur adipisicing elit.",
      },
      {
        id: 3,
        start_time: 15,
        end_time: 17,
        title:
          "Lorem, ipsum dolor sit amet consectetur adipisicing elit.",
      },
      {
        id: 4,
        start_time: 18,
        end_time: 22,
        title:
          "Lorem, ipsum dolor sit amet consectetur adipisicing elit. A, possimus.",
      },
      {
        id: 5,
        start_time: 23,
        end_time: 29,
        title:
          "Lorem, ipsum dolor sit amet consectetur adipisicing elit. A, possimus.",
      },
    ].map((subtitle) => ({
      ...subtitle,
      active:
        this.currentTimeVideo >= subtitle.start_time &&
        this.currentTimeVideo <= subtitle.end_time,
    }));
  },
  currentTimeVideo: 0,
  activeList: 0,

  player: undefined,

  mounted() {
    window.onYouTubePlayerAPIReady = this.onYouTubePlayerAPIReady;
  },

  onYouTubePlayerAPIReady() {
    this.player = new YT.Player("ytplayer", {
      height: "400",
      width: "800",
      videoId: "fuPX8mjeb-E",
    });
    var iframeWindow = this.player.getIframe().contentWindow;

    // So we can compare against new updates.
    let lastTimeUpdate = 0;

    window.addEventListener("message", (event) => {
      // Check that the event was sent from the YouTube IFrame.
      if (event.source === iframeWindow) {
        var data = JSON.parse(event.data);

        // The "infoDelivery" event is used by YT to transmit any
        // kind of information change in the player,
        // such as the current time or a playback quality change.
        if (
          data.event === "infoDelivery" &&
          data.info &&
          data.info.currentTime
        ) {
          // currentTime is emitted very frequently,
          // but we only care about whole second changes.
          var time = Math.floor(data.info.currentTime);
          if (time !== lastTimeUpdate) {
            lastTimeUpdate = time;
            this.currentTimeVideo = time;
          }
        }
      }
    });
  },
  Subtitle(item) {
    return {
      $template: "#item",
      isEdit: 0,

      handleClickSubtitle(second) {
        this.player.seekTo(second);
      },
      deleteItem(id) {
        alert("delete");
      },
      saveSubtitle(id) {
        this.isEdit = 0;
        const sbText = document.getElementById(`sb-${id}`);
        this.subtitlesList.forEach((item) => {
          if (item.id == id) {
            item.title = sbText.innerText;
          }
        });
      },
      handleEdit(id) {
        this.isEdit = id;
        const sbText = document.getElementById(`sb-${id}`);
        sbText.focus();
      },
    };
  },
}).mount();