using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.IO;

namespace Platformer
{
    /// <summary>
    /// Simple telemetry server proxy (Windows and Windows Phone only).
    /// Used to add several gameplay events to the server
    /// </summary>
    public class TelemetryProxy
    {
        private Microsoft.Xna.Framework.Game game;
        private String serverURL;

        

        public TelemetryProxy(Microsoft.Xna.Framework.Game game, String serverURL)
        {
            this.game = game;
            this.serverURL = serverURL;
        }

        /// <summary>
        /// Push a given gameplay event to the telemetry server
        /// </summary>
        public void AddGameplayEvent(TelemetryEvent telemetryEvent)
        {
            SendRequest(telemetryEvent.ToJSON());
        }

        /// <summary>
        /// Send a plain post request to the server
        /// </summary>
        private void SendRequest(String postData)
        {
            // Create a request using a URL that can receive a post. 
            WebRequest request = WebRequest.Create(this.serverURL);
            // Set the Method property of the request to POST.
            request.Method = "POST";
            byte[] byteArray = Encoding.UTF8.GetBytes(postData);
            // Set the ContentType property of the WebRequest.
            request.ContentType = "application/x-www-form-urlencoded";
            // Set the ContentLength property of the WebRequest.
            request.ContentLength = byteArray.Length;
            // Get the request stream.
            Stream dataStream = request.GetRequestStream();
            // Write the data to the request stream.
            dataStream.Write(byteArray, 0, byteArray.Length);
            // Close the Stream object.
            dataStream.Close();
            // Get the response.
            WebResponse response = request.GetResponse();
            // Display the status.
            Console.WriteLine(((HttpWebResponse)response).StatusDescription);
            // Get the stream containing content returned by the server.
            dataStream = response.GetResponseStream();
            // Open the stream using a StreamReader for easy access.
            StreamReader reader = new StreamReader(dataStream);
            // Read the content.
            string responseFromServer = reader.ReadToEnd();
            // Display the content.
            Console.WriteLine(responseFromServer);
            // Clean up the streams.
            reader.Close();
            dataStream.Close();
            response.Close();
        }
    }
}
