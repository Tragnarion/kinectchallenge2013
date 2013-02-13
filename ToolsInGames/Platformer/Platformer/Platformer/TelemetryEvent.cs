using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Platformer
{
    /// <summary>
    /// Type of events that we can handle
    /// </summary>
    enum EventType
    {
        Kill,
        Death,
        LevelStart,
        LevelEnd
    };

    /// <summary>
    /// Basic event. Base interface to connect to our JSON RPC server
    /// </summary>
    public abstract class TelemetryEvent
    {
        /// <summary>
        /// Build a JSON string from the event data
        /// </summary>
        /// <returns></returns>
        public String ToJSON()
        {
            // Create a json object from this event and then stringigy it
            JSONObject json = new JSONObject();
            json.AddField("jsonrpc", "2.0");

            // We always use id 1, no async tasks are required
            json.AddField("id", 1);

            // Add metod name
            json.AddField("method", GetMethodName());
            json.AddField("params", GetParams());

            return json.ToString();
        }

        /// <summary>
        /// Build the params JSON object to be send to the server
        /// </summary>
        /// <returns>JSONObject</returns>
        abstract protected JSONObject GetParams();

        /// <summary>
        /// Get the methond name the event will use
        /// </summary>
        /// <returns>String</returns>
        abstract protected String GetMethodName();
    }
}
