
indexbot=1
server = HttpServer.new()



server:setLogger(function(request, response)
  print(string.format("Method: %s, Path: %s, Status: %i", request.method, request.path, response.status))
end)

server:get("/bot/degsgs", function(request, response)
    world=request:getParam("world")
    indexbot=1
    tokenLu="kontol"
    
    bot=getBots()[indexbot]
    function valueToJson(v)
        if type(v) == "string" then
            return '"' .. v:gsub('"', '\\"') .. '"'
        elseif type(v) == "number" then
            return tostring(v)
        elseif type(v) == "boolean" then
            return v and "true" or "false"
        elseif type(v) == "table" then
            return tableToJson(v)
        else
            return '"' .. tostring(v) .. '"'
        end
    end
    
    function tableToJson(tbl)
        local is_array = true
        for k in pairs(tbl) do
            if type(k) ~= "number" then
                is_array = false
                break
            end
        end
        
        local result = {}
        
        if is_array then
            -- Format sebagai array JSON
            for i, v in ipairs(tbl) do
                table.insert(result, valueToJson(v))
            end
            return "[" .. table.concat(result, ",") .. "]"
        else
            local first = true
            for k, v in pairs(tbl) do
                if not first then
                    table.insert(result, ",")
                end
                first = false
                
                table.insert(result, '"' .. tostring(k) .. '":' .. valueToJson(v))
            end
            return "{" .. table.concat(result) .. "}"
        end
    end
    
    
    function scanWorld(world)
        if bot.status ~= 1 then
            return '{ "status": false,"message": "Bot is offline <a:offline:1397515323774603354>" }'
        objectlist={}
        bot:warp(world)
        sleep(4500)
        if bot:getWorld().name ~= world:upper() then
            bot:warp("exit")
            return '{ "status": false,"message": "cannont warp please check world and try again" }'
        end
        
        growscan=bot:getWorld().growscan
        for id,counts in pairs(growscan:getObjects()) do
            table.insert(objectlist,{
                tipe="object",
                count=counts,
                name=getInfo(id).name
            })
        end
        for id,counts in pairs(growscan:getTiles()) do
            table.insert(objectlist,{
                tipe="block",
                count=counts,
                name=getInfo(id).name
            })
        end
        bot:warp("exit")
        return tableToJson(objectlist)
    end 
    
    if world==nil then
        return response:setContent('{ "status": false,"message": "enter world lol" }',"application/json")
    else
        if request:getParam("token") == tokenLu then
            return response:setContent(scanWorld(world),"application/json")
        else
            return response:setContent('{ "status": false,"message": "Wrong Token LOL." }',"application/json")
        end
    end
end)

server:listen("0.0.0.0", 5000)

