_tostring = 
    function (...) 
        ret = {}
        for _,v in pairs({...}) do
            print(string.len(tostring(v)))
            table.insert(ret, tostring(v))
        end
        for _,v in pairs(ret) do
            print(v)
        end
        return table.unpack(ret)
    end
