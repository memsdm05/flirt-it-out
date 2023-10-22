using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using NativeWebSocket;
using Newtonsoft.Json;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    //websocket
    WebSocket websocket;
    public bool websocketOpen = false;

    //heartsAnim
    public Animator heartsAnim;

    //canvases
    public Canvas titleCanvas, lobbyCanvas, gameCanvas, leaderboardCanvas, endGameCanvas;

    //settings for stretch goal, default round num is 3 and duration is 90 secs
    public int rounds = 3;
    public int duration = 90;

    //gamecanvas stuff
    //timerbar game object with time bar inside it
    public RawImage timeBarBackground, time;
    //curTime is used to determine how much time passed since websocket to server when round starts, round time is time in 1 round
    public float curTime = 0f;
    public float roundTime = 90f;
    public bool anim_end_bool = false;
    public string timeGlobal, botName;
    public TextMeshProUGUI botNameText;

    //leaderboard stuff
    public List<string> playersScoresArr = new List<string>();
    public TextMeshProUGUI player1, player2, player3, player4, player5, player6, player7, player8;

    // Start is called before the first frame update
    async void Start()
    {
        Debug.Log("start method  start");
        lobbyCanvas.enabled = false;
        timeBarBackground.enabled = false;
        time.enabled = false;
        gameCanvas.enabled = false;
        gameCanvas.GetComponent<Animator>().enabled = false;
        leaderboardCanvas.enabled = false;
        leaderboardCanvas.GetComponent<Animator>().enabled = false;
        botNameText.enabled = false;
        //endGameCanvas.enabled = false;

        /* Websocket Stuff
        Debug.Log("Attempt to connect to websocket");
        websocket = new WebSocket("ws://104.39.33.21:6969/echo");

        websocket.OnOpen += () =>
        {
            Debug.Log("Connection open!");
        };

        websocket.OnError += (e) =>
        {
            Debug.Log("Error! " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Connection closed!");
        };

        websocket.OnMessage += (bytes) =>
        {
            //Debug.Log("OnMessage!");
            //Debug.Log(bytes);

            // getting the message as a string
            var message = System.Text.Encoding.UTF8.GetString(bytes);
            Debug.Log("OnMessage! " + message);
        };

        // Keep sending messages at every 0.3s
        //InvokeRepeating("SendWebSocketMessage", 0.0f, 0.3f);

        // waiting for messages
        await websocket.Connect();
        */
    }

    void Update()
    {
        if(websocketOpen)
        {
            //websocket stuff
            #if !UNITY_WEBGL || UNITY_EDITOR
                        websocket.DispatchMessageQueue();
            #endif
        }


        //quit app by pressing esc
        if (lobbyCanvas.enabled && Input.GetKeyDown(KeyCode.Escape))
        {
            Debug.Log("Quit app");
            Application.Quit();
        }

        //lobby screen transition
        if (titleCanvas.enabled && Input.GetKeyDown(KeyCode.Return))
        {
            Debug.Log("title screen transition to lobby");
            StartCoroutine(canvasTransition(titleCanvas, lobbyCanvas));
        }

        //game screen transition
        if (lobbyCanvas.enabled && Input.GetKeyDown(KeyCode.Return))
        {
            Debug.Log("lobbyCanvas to game");
            StartCoroutine(canvasTransition(lobbyCanvas, gameCanvas));
        }

        //increases curTime once anim_end_bool is true (once we send packet to server)
        if(anim_end_bool && curTime < 90f)
        {
            curTime += Time.deltaTime*10f; //TEMP *10 FOR TESTING
        }
        else if(curTime > 90f)
        {
            curTime = 90f;
        }

        //update timer bar based on time given
        if(gameCanvas.enabled && time.enabled)
        {
            time.transform.localScale = new Vector3((roundTime-curTime)/roundTime,1,1);
            //Debug.Log(time.transform.localScale.x);
        }

        //leaderboard screen transition
        //if get packet while game canvas is enabled after timer starts counting down then transition to leaderboard canvas
        if(gameCanvas.enabled && (time.transform.localScale.x <= .1f | Input.GetKeyDown(KeyCode.Return)))
        {
            StartCoroutine(canvasTransition(gameCanvas, leaderboardCanvas));
            Debug.Log("Game canvas to leaderboard canvas activated");
        }

        //back to lobbyScreen from leaderboard
        if (leaderboardCanvas.enabled == true && Input.GetKeyDown(KeyCode.Return))
        {
            Debug.Log("leaderboardCanvas to lobby");
            StartCoroutine(canvasTransition(leaderboardCanvas, lobbyCanvas));
            //RESET ANY VARS HERE THAT NEED RESET BETWEEN GAMES (player scores = 0? unless setting bassed on packet everytime)
            anim_end_bool = false;
            curTime = 0;
            playersScoresArr.Clear();
            SceneManager.LoadSceneAsync("Title");
        }
    }

    async void SendWebSocketMessage()
    {
        if (websocket.State == WebSocketState.Open)
        {
            // Sending bytes
            //await websocket.Send(new byte[] { 10, 20, 30 });

            // Sending plain text
            await websocket.SendText("Sup cutie ;)");
        }
    }

    private async void OnApplicationQuit()
    {
        await websocket.Close();
    }

    public IEnumerator canvasTransition(Canvas canvasToDisable, Canvas canvasToEnable)
    {
        Debug.Log("canvasTransition method used");
        heartsAnim.SetTrigger("FadeIn");

        //if title canvas enabled connect to websocket at that point
        if (titleCanvas.enabled)
        {
            ConnectToWebsocket();
        }

        yield return new WaitForSeconds(1f);

        canvasToDisable.enabled = false;
        canvasToEnable.enabled = true;
        heartsAnim.SetTrigger("FadeOut");

        //if switching to gameCanvas, start flirt it out text animation as soon as canvas exists
        if (canvasToEnable == gameCanvas)
        {
            botNameText.enabled = false;
            //time waited before fadeout completes is done in the actual animation
            gameCanvas.GetComponent<Animator>().enabled = true;
            yield return new WaitForSeconds(4.5f);
            Debug.Log("anim over now!");
            botNameText.enabled = true;
            //WEBSOCKET ANIM_END SEND TO SERVER
            anim_end_bool = true;
            SendJsonStringStartGame();
            time.enabled = true;
            timeBarBackground.enabled = true;
        }

        if (canvasToEnable == leaderboardCanvas)
        {
            leaderboardCanvas.GetComponent<Animator>().enabled = true;
        }

    }

    [System.Serializable]
    public class StartRoundVars
    {
        public string ends_at;
        public string bot_name;
    }

    [System.Serializable]
    public class StartRoundVarsPacket
    {
        public string action;
        public StartRoundVars payload;
    }

    [System.Serializable]
    public class Leaderboard
    {
        public List<LeaderboardData> leaderboardData;
    }

    [System.Serializable]
    public class LeaderboardPacket
    {
        public string action;
        public Leaderboard leaderboard;
    }

    [System.Serializable]
    public class LeaderboardData
    {
        public string player;
        public float score;
    }

    async void ConnectToWebsocket()
    {
        websocket = new WebSocket("ws://104.39.33.21:8080/host");
        
        websocket.OnOpen += () =>
        {
            Debug.Log("Connection open!");
            websocketOpen = true;
        };

        websocket.OnError += (e) =>
        {
            Debug.Log("Error! " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Connection closed!");
        };

        websocket.OnMessage += (bytes) =>
        {
            //Debug.Log("OnMessage!");
            //Debug.Log(bytes);

            //getting the message as a string and deserialize it into a packet, then find the current action of that packet
            var message = System.Text.Encoding.UTF8.GetString(bytes);
            Debug.Log("OnMessage! " + message);
            StartRoundVarsPacket packet = JsonConvert.DeserializeObject<StartRoundVarsPacket>(message);
            //packet.payload.bot_name = botname
            //packet.payload.ends_at = ends_at
            //var action = (string)packet["action"];
            //Debug.Log(action);
            //Debug.Log(packet["payload"]);
            //var payloadStr = ((Dictionary<string, object>)packet["payload"]);
            //Debug.Log(payloadStr);
            //Dictionary<string, object> payload = JsonConvert.DeserializeObject<Dictionary<string,object>>(payloadStr);
            if (packet.action == "hello")
            {
                Debug.Log("hello world, websocket");
            }
            else if(JsonConvert.DeserializeObject<StartRoundVarsPacket>(message).action == "start_round")
            {
                Debug.Log(packet.payload.bot_name);
                botNameText.text = packet.payload.bot_name;
                Debug.Log(packet.payload.ends_at);
                timeGlobal = packet.payload.ends_at;
                Debug.Log("start_round json packet var's gotten timeglobal: " + timeGlobal + "\nbot_name = " + botName);
            }
            else if(JsonConvert.DeserializeObject<LeaderboardPacket>(message).action == "scores")
            {
                LeaderboardPacket packetScores = JsonConvert.DeserializeObject<LeaderboardPacket>(message);
                foreach(LeaderboardData data in packetScores.leaderboard.leaderboardData)
                {
                    playersScoresArr.Add(data.player + ": " + data.score);
                }
                List<TextMeshProUGUI> playersStrings = new List<TextMeshProUGUI> { player1, player2, player3, player4, player5, player6, player7, player8 };
                int i = 0;

                foreach(string player in playersScoresArr)
                {
                    playersStrings[i].text = player;
                    i++;
                }
            }
        };

        // Keep sending messages at every 0.3s
        //InvokeRepeating("SendWebSocketMessage", 0.0f, 0.3f);

        // waiting for messages
        await websocket.Connect();
    }

    async void SendJsonString()
    {
        if (websocket.State == WebSocketState.Open)
        {
            // Create a dictionary to represent the JSON object
            Dictionary<string, object> jsonData = new Dictionary<string, object>
            {
                { "action", "anim_end" },
                { "payload", new Dictionary<string, object>
                    {

                    }
                }
            };

            // Serialize the dictionary to a JSON string
            string jsonString = JsonConvert.SerializeObject(jsonData);
            // Sending plain text
            await websocket.SendText(jsonString);
            Debug.Log("Sent JSON String");
        }
    }

    async void SendJsonStringStartGame()
    {
        if (websocket.State == WebSocketState.Open)
        {
            // Create a dictionary to represent the JSON object
            Dictionary<string, object> jsonData = new Dictionary<string, object>
            {
                { "action", "start_game" },
                { "payload", new Dictionary<string, object>
                    {
                        //{"rounds", },
                        //{"duration", }
                    }
                }
            };

            // Serialize the dictionary to a JSON string
            string jsonString = JsonConvert.SerializeObject(jsonData);
            // Sending plain text
            await websocket.SendText(jsonString);
            Debug.Log("Sent JSON String");
        }
    }
}
