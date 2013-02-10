using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Platformer
{
    enum EventType
    {
        Kill,
        Death,
        LevelStart,
        LevelEnd
    };

    public abstract class TelemetryEvent
    {
        public String ToJSON()
        {
            {
                "jsonrpc": "2.0", 
                "method": GetEventName(), 
                "params": {
                    SerializeEvent()()
                },
                "id": 1
            }
        }

        abstract protected String SerializeEvent();
        abstract protected String GetEventName();
    }
}
