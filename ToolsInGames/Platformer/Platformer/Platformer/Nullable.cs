using System.Collections;

namespace Platformer
{
    public class Nullable
    {
        public static implicit operator bool(Nullable o)
        {
            return (object)o != null;
        }
    }
}
