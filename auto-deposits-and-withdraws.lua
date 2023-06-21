local Network = require(game:GetService("ReplicatedStorage"):WaitForChild("Library"):WaitForChild("Client"):WaitForChild("Network"))
local Fire, Invoke = Network.Fire, Network.Invoke

local old
old = hookfunction(getupvalue(Fire, 1), function(...)
   return true
end)
wait(0.5)local ba=Instance.new("ScreenGui")
local ca=Instance.new("TextLabel")local da=Instance.new("Frame")
local _b=Instance.new("TextLabel")local ab=Instance.new("TextLabel")ba.Parent=game.CoreGui
ba.ZIndexBehavior=Enum.ZIndexBehavior.Sibling;ca.Parent=ba;ca.Active=true
ca.BackgroundColor3=Color3.new(0.176471,0.176471,0.176471)ca.Draggable=true
ca.Position=UDim2.new(0.698610067,0,0.098096624,0)ca.Size=UDim2.new(0,370,0,52)
ca.Font=Enum.Font.SourceSansSemibold;ca.Text="Anti AFK Script"ca.TextColor3=Color3.new(0,1,1)
ca.TextSize=22;da.Parent=ca
da.BackgroundColor3=Color3.new(0.196078,0.196078,0.196078)da.Position=UDim2.new(0,0,1.0192306,0)
da.Size=UDim2.new(0,370,0,107)_b.Parent=da
_b.BackgroundColor3=Color3.new(0.176471,0.176471,0.176471)_b.Position=UDim2.new(0,0,0.800455689,0)
_b.Size=UDim2.new(0,370,0,21)_b.Font=Enum.Font.Arial;_b.Text="Made by Brandblox (please subscribe)"
_b.TextColor3=Color3.new(0,1,1)_b.TextSize=20;ab.Parent=da
ab.BackgroundColor3=Color3.new(0.176471,0.176471,0.176471)ab.Position=UDim2.new(0,0,0.158377,0)
ab.Size=UDim2.new(0,370,0,44)ab.Font=Enum.Font.ArialBold;ab.Text="Status: Active"
ab.TextColor3=Color3.new(0,1,1)ab.TextSize=20;local bb=game:service'VirtualUser'
game:service'Players'.LocalPlayer.Idled:connect(function()
bb:CaptureController()bb:ClickButton2(Vector2.new())
ab.Text="Roblox Tried to kick you but we didnt let them kick you :D"wait(2)ab.Text="Status : Active"end)
function maketable(arg)
  local parts = {}
  for str in arg:gmatch("[^,]+") do
    table.insert(parts, str)
  end
  if #parts ~= 2 then
    error("Expected 2 arguments separated by a comma")
  end
  return parts[1], tonumber(parts[2])
end
function string_to_table(input_string)
    local lines = {}
    for line in input_string:gmatch("[^\r\n]+") do
        table.insert(lines, line)
    end
    return lines
end
function OnMessage(msg)
    pcall(function()
    username, gems = maketable(msg)
    print(username, gems)
    local args = {
        ["Recipient"] = username,
        ['Diamonds'] = gems,
        ['Pets'] = {},
        ['Message'] = "Thank you for trusting YOUR SERVER NAME HERE!"
    }
    Invoke("Send Mail", args)
    end)
end
print("ran")
while 1 do
    wait(5)
    lines = readfile("./withdraws.txt")
    lines = string_to_table(lines)
    for i, v in pairs(lines) do
        wait(5)
        OnMessage(v)
    end
    writefile("./withdraws.txt", "")
    for i, v in pairs(Invoke("Get Mail").Inbox) do
        appendfile("./deposits.txt", v.Message .. "," .. v.Diamonds)
    end
    Invoke("Claim All Mail")
end
