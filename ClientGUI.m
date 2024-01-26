classdef ClientGUI < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        AudioServerClientGUIUIFigure    matlab.ui.Figure
        TabGroup                        matlab.ui.container.TabGroup
        PlaybackTab                     matlab.ui.container.Tab
        GridLayout7                     matlab.ui.container.GridLayout
        PlaybackLamp                    matlab.ui.control.Lamp
        PlaybackTypeSwitch              matlab.ui.control.Switch
        FromFilesPanel                  matlab.ui.container.Panel
        GridLayoutFromFiles             matlab.ui.container.GridLayout
        SeeInfoButton                   matlab.ui.control.Button
        FromFilesPanelInfo              matlab.ui.control.Label
        PlaybackRefreshListsButton      matlab.ui.control.Button
        FilterPanel                     matlab.ui.container.Panel
        GridLayoutPlaybackFilter        matlab.ui.container.GridLayout
        FilterAudioFilesButton          matlab.ui.control.StateButton
        FilterPlaylistsButton           matlab.ui.control.StateButton
        FromFileDropDown                matlab.ui.control.DropDown
        PlaythefilesAllRandomCheckBox   matlab.ui.control.CheckBox
        FromFileFileCountLabel          matlab.ui.control.Label
        FromFileFileCountSpinner        matlab.ui.control.Spinner
        FromFilePauseBetweenFilesmsLabel  matlab.ui.control.Label
        FromFileInterstimulusIntervalmsSpinner  matlab.ui.control.Spinner
        GaplessPlaybackCheckBox         matlab.ui.control.CheckBox
        PlayButtonFromFiles             matlab.ui.control.StateButton
        PlaybackFromFilesLogs           matlab.ui.control.TextArea
        GeneratePanel                   matlab.ui.container.Panel
        GridLayoutGenerate              matlab.ui.container.GridLayout
        SendtoCreateButton              matlab.ui.control.Button
        GeneratePanelInfo               matlab.ui.control.Label
        GenerateTypePanel               matlab.ui.container.Panel
        GridLayoutGenerateType          matlab.ui.container.GridLayout
        GenerateToneTypeButton          matlab.ui.control.StateButton
        GenerateSweepTypeButton         matlab.ui.control.StateButton
        FrequencyHzLabel                matlab.ui.control.Label
        FrequencyHzSpinner              matlab.ui.control.Spinner
        EndFrequencyHzLabel             matlab.ui.control.Label
        EndFrequencyHzSpinner           matlab.ui.control.Spinner
        DurationmsSpinner               matlab.ui.control.Spinner
        AmplitudedBSpinner              matlab.ui.control.Spinner
        SampleRateHzSpinner             matlab.ui.control.Spinner
        EdgesmsSpinner                  matlab.ui.control.Spinner
        EdgesmsSpinnerLabel             matlab.ui.control.Label
        SampleRateHzSpinnerLabel        matlab.ui.control.Label
        AmplitudedBSpinnerLabel         matlab.ui.control.Label
        DurationmsSpinnerLabel          matlab.ui.control.Label
        EdgesmsHelp                     matlab.ui.control.Label
        SweepFunctionLabel              matlab.ui.control.Label
        SweepFnDropDown                 matlab.ui.control.DropDown
        PlayButtonGenerateAudio         matlab.ui.control.StateButton
        PlaybackGenerateAudioLog        matlab.ui.control.TextArea
        CreateTab                       matlab.ui.container.Tab
        GridLayout2                     matlab.ui.container.GridLayout
        CreateLamp                      matlab.ui.control.Lamp
        CreateRandomPlaylist            matlab.ui.container.Panel
        GridLayout3                     matlab.ui.container.GridLayout
        QuicklyCreateaNewRandomPlaylistontheAudioServerLabel  matlab.ui.control.Label
        CreateRandomPlaylistInfo        matlab.ui.control.Label
        CreateFileCountLabel            matlab.ui.control.Label
        CreateFileCountSpinner          matlab.ui.control.Spinner
        CreatePauseBetweenFilesmsLabel  matlab.ui.control.Label
        CreateInterstimulusIntervalmsSpinner  matlab.ui.control.Spinner
        DownloadaCopyofThisPlaylistCheckBox  matlab.ui.control.CheckBox
        CreateButtonGeneratePlaylist    matlab.ui.control.StateButton
        ToneSweepPanel                  matlab.ui.container.Panel
        GridLayoutCreateToneSweep       matlab.ui.container.GridLayout
        CreateToneSweepInfo             matlab.ui.control.Label
        CreateTypeToneSweepPanel        matlab.ui.container.Panel
        GridLayoutCreateTypeToneSweep   matlab.ui.container.GridLayout
        CreateToneTypeButton            matlab.ui.control.StateButton
        CreateSweepTypeButton           matlab.ui.control.StateButton
        FrequencyHzLabel_2              matlab.ui.control.Label
        FrequencyHzSpinner_2            matlab.ui.control.Spinner
        EndFrequencyHzLabel_2           matlab.ui.control.Label
        EndFrequencyHzSpinner_2         matlab.ui.control.Spinner
        EdgesmsSpinner_2Label           matlab.ui.control.Label
        SampleRateHzSpinner_2Label      matlab.ui.control.Label
        AmplitudedBSpinner_2Label       matlab.ui.control.Label
        DurationmsSpinner_2             matlab.ui.control.Spinner
        DurationmsSpinner_2Label        matlab.ui.control.Label
        AmplitudedBSpinner_2            matlab.ui.control.Spinner
        SampleRateHzSpinner_2           matlab.ui.control.Spinner
        EdgesmsSpinner_2                matlab.ui.control.Spinner
        EdgesmsHelp_2                   matlab.ui.control.Label
        SweepFunctionLabel_2            matlab.ui.control.Label
        SweepFnDropDown_2               matlab.ui.control.DropDown
        CreateButtonGenerateToneSweep   matlab.ui.control.StateButton
        WindowsBatchFilesPanel          matlab.ui.container.Panel
        GridLayout5                     matlab.ui.container.GridLayout
        DownloadaszipButton             matlab.ui.control.StateButton
        BatchFilesInfo                  matlab.ui.control.Label
        BatchFilesDropDown              matlab.ui.control.DropDown
        InformationTab                  matlab.ui.container.Tab
        GridLayout                      matlab.ui.container.GridLayout
        PlaylistsInfoButton             matlab.ui.control.Button
        AudioFilesInfoButton            matlab.ui.control.Button
        InfoDropDown                    matlab.ui.control.DropDown
        AvailableAudioFilesPlaylistsButton  matlab.ui.control.Button
        MainAPIDocumentationButton      matlab.ui.control.Button
        InformationPanel                matlab.ui.control.TextArea
        SettingsTab                     matlab.ui.container.Tab
        GridLayoutSettings              matlab.ui.container.GridLayout
        PowerOptionsPanel               matlab.ui.container.Panel
        GridLayout6                     matlab.ui.container.GridLayout
        RestartServerLabel              matlab.ui.control.Label
        RestartButton                   matlab.ui.control.Button
        OrusetheURIbelowtoRestarttheservermanuallyLabel  matlab.ui.control.Label
        ManualRestartURI                matlab.ui.control.TextArea
        ShutdownServerLabel             matlab.ui.control.Label
        ShutdownButton                  matlab.ui.control.Button
        ServerIPPortEditField           matlab.ui.control.EditField
        ServerIPPortLabel               matlab.ui.control.Label
    end

    
    properties (Access = private)
        AudioFilesList % Collection of Available Audio Files
        PlaylistsList % Collection of Available (Validated) Playlists

        % Store the last state of file names or paths
        LastState = struct('PlaybackAudioName', '', 'PlaybackPlaylistName', '', 'SavePath', pwd);
    end
    
    methods (Access = private)

        function setStatusLampColor_tip(~, lampTarget, colorHex, tooltip)
        %SETSTATUSLAMPCOLOR Set color of the indicator lamp and display a message
        
            % preset colors, otherwise use the stated hex string in colorHex
            if colorHex == "orange"
                colorHex = "#edcdb2";
                if isempty(tooltip) || ~exist('tooltip','var')
                    tooltip = "Working...";
                end
            elseif colorHex == "green" || ~exist('tooltip','var')
                colorHex = "#bdd9b0";
                if isempty(tooltip)
                    tooltip = "Ready";
                end
            elseif colorHex == "red" || ~exist('tooltip','var')
                colorHex = "#b82121";
                if isempty(tooltip)
                    tooltip = "Error!";
                end
            end
        
            if ~isempty(tooltip)
                lampTarget.Tooltip = sprintf(tooltip);
            else
                lampTarget.Tooltip = "Status";
            end
        
            lampTarget.Color = colorHex;
        end

                
        function handle_HTTP_error(app, ME, callButtonOrigin, lampTarget, logBoxTarget)
            function reset_interface(callButtonOrigin, lampTarget)
                if isequal(class(callButtonOrigin),'matlab.ui.control.StateButton')
                    callButtonOrigin.Value = false;
                end
                
                callButtonOrigin.Enable = "on";
                if isempty(lampTarget)
                    return
                end
                setStatusLampColor_tip(app, lampTarget, "red", "Error sending API request. Please check the Command Window.");
            end

            reset_interface(callButtonOrigin, lampTarget);

            identifier = ME.identifier;
            message = ME.message;

            % if identifier is 'MATLAB:webservices:ConnectionRefused'
            % AND message ends with 'Recv failure: Connection was reset'
            % then the server was restarted successfully
            % Most likely the intended behavior
            if identifier == "MATLAB:webservices:ConnectionRefused" && endsWith(message, "Recv failure: Connection was reset")
                if ~isempty(logBoxTarget)
                    logBoxTarget.Value = sprintf("Connection was reset. If audio was playing, it should have been stopped.\nIf you were trying to restart the audio server to stop the playing audio but it did not work, you may need to stop the server manually.");
                end
            % if identifier is 'MATLAB:webservices:ConnectionRefused'
            % AND message ends with 'Couldn't connect to server'
            % then the server is not online or not reachable
            elseif identifier == "MATLAB:webservices:ConnectionRefused" && endsWith(message, "Couldn't connect to server")
                if ~isempty(logBoxTarget)
                    logBoxTarget.Value = sprintf("Cannot connect to the audio server. Is the audio server running and reachable?");
                end
                if ~isempty(lampTarget) 
                    setStatusLampColor_tip(app, lampTarget, "red", "Cannot connect to the audio server. Is the audio server running and reachable?\n\nTry to restart the server manually, or try to open the 'ServerIP:Port' address in a browser to check if the server is online.");
                
                end
            end
        end


        function response = app_HTTP_request(app, request, uri, callButtonOrigin, lampTarget, logBoxTarget)
            try
                response = send(request, uri);
                drawnow
            catch ME
                disp(ME)
                fprintf('Cannot send GET request, or the connection was interupted.\n\n')
                response.error = ME;

                handle_HTTP_error(app, ME, callButtonOrigin, lampTarget, logBoxTarget);
            end
        end

    end
   

    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app)
            format longG

            app.ManualRestartURI.Value = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), "/restart", '?restart=true');

            
            % Update the Information Panel with the API documentation
            request = matlab.net.http.RequestMessage;

            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/');
            response = app_HTTP_request(app, request, uri, app.MainAPIDocumentationButton, app.PlaybackLamp, app.InformationPanel);
            if isempty(response) || isfield(response, "error")
                % also update the CreateLamp
                setStatusLampColor_tip(app, app.CreateLamp, "#ad6ad9", "[App Start Up]: No audio server running on localhost:5055.\n\nIf you want to access the server from another machine, go to Settings and update the server IP address. Otherwise, make sure that the port number is correct. The IP + Port should be printed to the audio server's console when it started up.");
                setStatusLampColor_tip(app, app.PlaybackLamp, "#ad6ad9", "[App Start Up]: No audio server running on localhost:5055.\n\nIf you want to access the server from another machine, go to Settings and update the server IP address. Otherwise, make sure that the port number is correct. The IP + Port should be printed to the audio server's console when it started up.");
                return
            end
            PlaybackRefreshListsButtonPushed(app);
            app.InformationPanel.Value = response.Body.Data;
        end

        % Value changed function: PlaybackTypeSwitch
        function PlaybackTypeSwitchValueChanged(app, event)
            value = app.PlaybackTypeSwitch.Value;
            if value == "From Files"
                app.FromFilesPanel.Enable = "on";
                app.GeneratePanel.Enable = "off";
            elseif value == "Generate"
                app.GeneratePanel.Enable = "on";
                app.FromFilesPanel.Enable = "off";
            end
        end

        % Value changed function: FilterAudioFilesButton
        function FilterAudioFilesButtonValueChanged(app, event)
            if app.FilterPlaylistsButton.Value == 0
                app.FilterAudioFilesButton.Value = 1;
                return
            end

            app.FilterPlaylistsButton.Value = 0;
            app.FilterAudioFilesButton.Value = 1;

            % Turn on All random play for Audio files mode
            app.PlaythefilesAllRandomCheckBox.Visible = "on";
            PlaythefilesAllRandomCheckBoxValueChanged(app, event); % reuse this function to handle the toggling of sub children  

            
            % Filter function

            if isempty(app.AudioFilesList)
                app.PlaybackFromFilesLogs.Value = sprintf("No Audio Files available.");
                return
            end

            % Filter for only Audio Files and display on dropdown list
            % Update the current active Filter Dropdown
            app.FromFileDropDown.Items = app.AudioFilesList;
            if isempty(app.LastState.PlaybackAudioName) || ismember(app.LastState.PlaybackAudioName, app.AudioFilesList) == 0
                app.LastState.PlaybackAudioName = app.AudioFilesList(1);
            end
            app.FromFileDropDown.Value = app.LastState.PlaybackAudioName;
        end

        % Value changed function: FilterPlaylistsButton
        function FilterPlaylistsButtonValueChanged(app, event)
            if app.FilterAudioFilesButton.Value == 0
                app.FilterPlaylistsButton.Value = 1;
                return
            end

            app.FilterAudioFilesButton.Value = 0;
            app.FilterPlaylistsButton.Value = 1;

            % All random play is not available for Playlist
            allrandomCBValue = app.PlaythefilesAllRandomCheckBox.Value; % hold the checkbox value
            app.PlaythefilesAllRandomCheckBox.Value = 0;
            PlaythefilesAllRandomCheckBoxValueChanged(app, event); % reuse this function to handle the toggling of sub children
            app.PlaythefilesAllRandomCheckBox.Value = allrandomCBValue; % reset the value
            app.PlaythefilesAllRandomCheckBox.Visible = "off";


            % Filter function

            if isempty(app.PlaylistsList)
                app.PlaybackFromFilesLogs.Value = sprintf("No Playlists available.");
                return
            end

            % Filter for only Playlists and display on dropdown list
            % Update the current active Filter Dropdown
            app.FromFileDropDown.Items = app.PlaylistsList;

            if isempty(app.LastState.PlaybackPlaylistName) || ismember(app.LastState.PlaybackPlaylistName, app.PlaylistsList) == 0
                app.LastState.PlaybackPlaylistName = app.PlaylistsList(1);
            end
            app.FromFileDropDown.Value = app.LastState.PlaybackPlaylistName;
        end

        % Value changed function: FromFileDropDown
        function FromFileDropDownValueChanged(app, event)
            value = app.FromFileDropDown.Value;
            if app.FilterAudioFilesButton.Value == 1
                app.LastState.PlaybackAudioName = value;                
            elseif app.FilterPlaylistsButton.Value == 1
                app.LastState.PlaybackPlaylistName = value;
            end
        end

        % Button pushed function: PlaybackRefreshListsButton
        function PlaybackRefreshListsButtonPushed(app, event)
            app.PlaybackRefreshListsButton.Enable = "off";
            setStatusLampColor_tip(app, app.PlaybackLamp, "orange", "Loading available audio files and playlists...\nPlease wait for the this to complete before doing anything else!");

            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/list', '?json=true');
            app.PlaybackFromFilesLogs.Value = append('GET ', uri);
            drawnow
            
            getList = app_HTTP_request(app, request, uri, app.PlaybackRefreshListsButton, app.PlaybackLamp, app.PlaybackFromFilesLogs);
            if isempty(getList) || isfield(getList, "error")
                return
            end

            list = getList.Body.Data;
            % Update AudioFilesList and PlaylistsList
            app.AudioFilesList = list.audio;
            app.PlaylistsList = list.playlist;

            app.PlaybackFromFilesLogs.Value = append('Status: ', string(getList.StatusLine), newline, jsonencode(list, "PrettyPrint", true));

            % Update the current active Filter Dropdown
            if ~isempty(app.AudioFilesList) || ~isempty(app.PlaylistsList)
                if app.FilterAudioFilesButton.Value == 1
                    if ~isempty(app.AudioFilesList)
                        app.FromFileDropDown.Items = app.AudioFilesList;
                        if isempty(app.LastState.PlaybackAudioName) || ismember(app.LastState.PlaybackAudioName, app.AudioFilesList) == 0
                            app.LastState.PlaybackAudioName = app.AudioFilesList(1);
                        end
                        app.FromFileDropDown.Value = app.LastState.PlaybackAudioName;
                    else
                        app.FromFileDropDown.Items = "";
                        app.FromFileDropDown.Value = '';
                        app.FilterAudioFilesButton.Value = 0;
                        app.FilterPlaylistsButton.Value = 1;
                    end
                    
                elseif app.FilterPlaylistsButton.Value == 1
                    if ~isempty(app.PlaylistsList)
                        app.FromFileDropDown.Items = app.PlaylistsList;
                        if isempty(app.LastState.PlaybackPlaylistName) || ismember(app.LastState.PlaybackPlaylistName, app.PlaylistsList) == 0
                            app.LastState.PlaybackPlaylistName = app.PlaylistsList(1);
                        end
                        app.FromFileDropDown.Value = app.LastState.PlaybackPlaylistName;
                    else
                        app.FromFileDropDown.Items = "";
                        app.FromFileDropDown.Value = '';
                        app.FilterPlaylistsButton.Value = 0;
                        app.FilterAudioFilesButton.Value = 1;
                    end
                end
            else
                app.FromFileDropDown.Items = "";
                app.FromFileDropDown.Value = '';
                app.PlaybackFromFilesLogs.Value = sprintf("No Audio Files or Playlists available.\n\nYou may still use the Generate Panel below instead.");
            end

            
            app.PlaybackRefreshListsButton.Enable = "on";
            setStatusLampColor_tip(app, app.PlaybackLamp, "green", "Ready!");
        end

        % Value changed function: PlaythefilesAllRandomCheckBox
        function PlaythefilesAllRandomCheckBoxValueChanged(app, event)
            value = app.PlaythefilesAllRandomCheckBox.Value;
            if value
                app.FromFileDropDown.Enable = "off";
                app.SeeInfoButton.Enable = "off";
                app.PlaythefilesAllRandomCheckBox.FontWeight = 'bold';
                app.FromFileFileCountLabel.Visible = "on";
                app.FromFileFileCountSpinner.Visible = "on";
                app.FromFilePauseBetweenFilesmsLabel.Visible = "on";
                app.FromFileInterstimulusIntervalmsSpinner.Visible = "on";
                % app.GaplessPlaybackCheckBox.Visible = "on";
            else
                app.FromFileDropDown.Enable = "on";
                app.SeeInfoButton.Enable = "on";
                app.PlaythefilesAllRandomCheckBox.FontWeight = 'normal';
                app.FromFileFileCountLabel.Visible = "off";
                app.FromFileFileCountSpinner.Visible = "off";
                app.FromFilePauseBetweenFilesmsLabel.Visible = "off";
                app.FromFileInterstimulusIntervalmsSpinner.Visible = "off";
                % app.GaplessPlaybackCheckBox.Visible = "off";
            end
        end

        % Value changed function: PlayButtonFromFiles
        function PlayButtonFromFilesValueChanged(app, event)
            app.PlayButtonFromFiles.Enable = "off";
            setStatusLampColor_tip(app, app.PlaybackLamp, "orange", "Playing Audio...\n\nThe audio cannot be stopped until it is finished, unless the server is shutdown.\nPlease wait for the playback to complete before doing anything else!");

            if app.FilterAudioFilesButton.Value == 1
                requestType = 'play';
            elseif app.FilterPlaylistsButton.Value == 1
                requestType = 'playlist';
            end
            
            if requestType == "play" && app.PlaythefilesAllRandomCheckBox.Value
                audio = "random";
            else
                audio = app.FromFileDropDown.Value;
            end

            if isempty(audio) || (audio == "random" && isempty(app.AudioFilesList))
                if audio == "random"
                    app.PlaybackFromFilesLogs.Value = sprintf("No audio files are available to be played.\nMake sure the audio server is started and reachable, then hit the 'Refresh Lists' button to get the available audio files and playlists. If there still isn't any audio file available, add some .wav files to the Audio Server ./audio/ folder, restart the server, and try again.");
                    setStatusLampColor_tip(app, app.PlaybackLamp, "red", "No audio files are available to be played.");
                else
                    app.PlaybackFromFilesLogs.Value = sprintf("An audio file or playlist must be selected.\nMake sure the audio server is started and reachable, then hit the 'Refresh Lists' button.");
                    setStatusLampColor_tip(app, app.PlaybackLamp, "red", "An audio file or playlist must be selected.");
                end

                app.PlayButtonFromFiles.Value = false;
                app.PlayButtonFromFiles.Enable = "on";
                return
            end

            request = matlab.net.http.RequestMessage;
            if audio == "random"
                file_count = app.FromFileFileCountSpinner.Value;
                break_between_files = app.FromFileInterstimulusIntervalmsSpinner.Value;
                uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/', requestType, '/', audio, ...
                    "?file_count=", num2str(file_count), "&break_between_files=", num2str(break_between_files), '&time=');
            else
                uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/', requestType, '/', audio, '?time=');
            end
            
            timeMicro = string(posixtime(datetime('now', TimeZone = 'local', Format = 'yyyy-MM-dd HH:mm:ss.SSSSSS'))*1000000);
            uri = strcat(uri, timeMicro, '000');
            app.PlaybackFromFilesLogs.Value = append('GET ', uri);
            drawnow
            
            response = app_HTTP_request(app, request, uri, app.PlayButtonFromFiles, app.PlaybackLamp, app.PlaybackFromFilesLogs);
            if isempty(response) || isfield(response, "error")
                return
            end

            app.PlaybackFromFilesLogs.Value = append('Status: ', string(response.StatusLine), newline, jsonencode(response.Body.Data, "PrettyPrint", true));

            app.PlayButtonFromFiles.Value = false;
            app.PlayButtonFromFiles.Enable = "on";
            setStatusLampColor_tip(app, app.PlaybackLamp, "green", "Ready!");
        end

        % Button pushed function: SeeInfoButton
        function SeeInfoButtonPushed(app, event)
            % Check for the type of the file in the dropdown
            % then trigger the Info button of that type
            % lastly, select the file in the Info Dropdown
            % and shift focus to the Info tab

            if app.FilterAudioFilesButton.Value == 1 % audio
                AudioFilesInfoButtonPushed(app, event)
                if ~ismember(app.FromFileDropDown.Value, app.AudioFilesList) == 1
                    % This audio file is no longer available
                    refresh_decision = uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('This audio file is no longer exist or available on the server. You should refresh the current list now.'), ...
                        'File Not Found', ...
                        "Options",["↺ Refresh List", "Later"], ...
                        "DefaultOption",1,"CancelOption",2, ...
                        "Icon","error");
                    if refresh_decision == "↺ Refresh List"
                        PlaybackRefreshListsButtonPushed(app, event);
                    end
                    return
                end

                % Everything is valid --> update value
                app.InfoDropDown.Value = app.FromFileDropDown.Value;
            elseif app.FilterPlaylistsButton.Value == 1 % playlist
                PlaylistsInfoButtonPushed(app, event)
                if ~ismember(app.FromFileDropDown.Value, app.PlaylistsList) == 1
                    % This playlist is no longer available
                    refresh_decision = uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('This playlist is no longer exist or available on the server. You should refresh the current list now.'), ...
                        'Playlist Not Found', ...
                        "Options",["↺ Refresh List", "Later"], ...
                        "DefaultOption",1,"CancelOption",2, ...
                        "Icon","error");
                    if refresh_decision == "↺ Refresh List"
                        PlaybackRefreshListsButtonPushed(app, event);
                    end
                    return
                end

                % Everything is valid --> update value
                app.InfoDropDown.Value = app.FromFileDropDown.Value;
            end

            % shift focus to the Info tab and get the info
            tabHandle = app.TabGroup.Children(3);
            app.TabGroup.SelectedTab = tabHandle;

            InfoDropDownValueChanged(app, event)
        end

        % Value changed function: GenerateToneTypeButton
        function GenerateToneTypeButtonValueChanged(app, event)
            if app.GenerateSweepTypeButton.Value == 0
                app.GenerateToneTypeButton.Value = 1;
                return
            end
            app.GenerateSweepTypeButton.Value = 0;
            app.GenerateToneTypeButton.Value = 1;

            % Disable End Freq, Sweep Type options,
            % Also rename Start Frequency to just Frequency
            app.FrequencyHzLabel.Text = "Frequency (Hz)";
            app.EndFrequencyHzLabel.Enable = "off";
            app.EndFrequencyHzSpinner.Enable = "off";
            app.SweepFunctionLabel.Enable = "off";
            app.SweepFnDropDown.Enable = "off";

            ToneSweepParamsValueChanged(app, event)
        end

        % Value changed function: GenerateSweepTypeButton
        function GenerateSweepTypeButtonValueChanged(app, event)
            if app.GenerateToneTypeButton.Value == 0
                app.GenerateSweepTypeButton.Value = 1;
                return
            end
            app.GenerateToneTypeButton.Value = 0;
            app.GenerateSweepTypeButton.Value = 1;

            % Enable End Freq, Sweep Type options,
            % Also rename Frequency to Start Frequency
            app.FrequencyHzLabel.Text = "Start Frequency (Hz)";
            app.EndFrequencyHzLabel.Enable = "on";
            app.EndFrequencyHzSpinner.Enable = "on";
            app.SweepFunctionLabel.Enable = "on";
            app.SweepFnDropDown.Enable = "on";

            ToneSweepParamsValueChanged(app, event)
        end

        % Value changed function: AmplitudedBSpinner, 
        % ...and 13 other components
        function ToneSweepParamsValueChanged(app, event)
            %% Composite function that triggers when any of the params in the Playback > Generate OR Create > Tone & Sweep panel changed
            % Compare the Playback tab with the Create tab. If any param is
            % different > Change the ✔ icon (last character) of the 
            % Send to Createbutton Text to ➥ --> suggest send

            % Tone params
            paramsPlayback = [
                app.FrequencyHzSpinner.Value, ...
                app.DurationmsSpinner.Value,...
                app.AmplitudedBSpinner.Value,...
                app.SampleRateHzSpinner.Value,...
                app.EdgesmsSpinner.Value
            ];
            paramsCreate = [
                app.FrequencyHzSpinner_2.Value, ...
                app.DurationmsSpinner_2.Value,...
                app.AmplitudedBSpinner_2.Value,...
                app.SampleRateHzSpinner_2.Value,...
                app.EdgesmsSpinner_2.Value
            ];

            if app.GenerateSweepTypeButton.Value == 1
                % Sweep params
                paramsPlayback = [paramsPlayback, app.EndFrequencyHzSpinner.Value, app.SweepFnDropDown.Value];
                paramsCreate = [paramsCreate, app.EndFrequencyHzSpinner_2.Value, app.SweepFnDropDown_2.Value];

                if ~isequal(paramsPlayback, paramsCreate)
                    app.SendtoCreateButton.Text = append(app.SendtoCreateButton.Text(1:end-1), '➥');
                else
                    app.SendtoCreateButton.Text = append(app.SendtoCreateButton.Text(1:end-1), '✔');
                end
            elseif app.GenerateToneTypeButton.Value == 1
                if ~isequal(paramsPlayback, paramsCreate)
                    app.SendtoCreateButton.Text = append(app.SendtoCreateButton.Text(1:end-1), '➥');
                else
                    app.SendtoCreateButton.Text = append(app.SendtoCreateButton.Text(1:end-1), '✔');
                end
            end
        end

        % Value changed function: PlayButtonGenerateAudio
        function PlayButtonGenerateAudioValueChanged(app, event)
            app.PlayButtonGenerateAudio.Enable = "off";
            setStatusLampColor_tip(app, app.PlaybackLamp, "orange", "Playing Audio...\n\nThe audio cannot be stopped until it is finished, unless the server is shutdown.\nPlease wait for the playback to complete before doing anything else!");

            % make route from params
            if app.GenerateToneTypeButton.Value == 1
                requestType = 'tone';
                data = strcat(num2str(app.FrequencyHzSpinner.Value), '/', num2str(app.DurationmsSpinner.Value), '/', ...
                    num2str(app.AmplitudedBSpinner.Value), '/', num2str(app.SampleRateHzSpinner.Value));
            elseif app.GenerateSweepTypeButton.Value == 1
                requestType = 'sweep';
                data = strcat(lower(app.SweepFnDropDown.Value), '/', num2str(app.FrequencyHzSpinner.Value), '/', ...
                    num2str(app.EndFrequencyHzSpinner.Value), '/', num2str(app.DurationmsSpinner.Value), '/', ...
                    num2str(app.AmplitudedBSpinner.Value), '/', num2str(app.SampleRateHzSpinner.Value));
            end

            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/', requestType, '/', data, '?time=');

            timeMicro = string(posixtime(datetime('now', TimeZone = 'local', Format = 'yyyy-MM-dd HH:mm:ss.SSSSSS'))*1000000);
            uri = strcat(uri, timeMicro, '000', '&edge=', num2str(app.EdgesmsSpinner.Value));
            app.PlaybackGenerateAudioLog.Value = append('GET ', uri);
            drawnow
            
            response = app_HTTP_request(app, request, uri, app.PlayButtonGenerateAudio, app.PlaybackLamp, app.PlaybackGenerateAudioLog);
            if isempty(response) || isfield(response, "error")
                return
            end

            app.PlaybackGenerateAudioLog.Value = append('Status: ', string(response.StatusLine), newline, jsonencode(response.Body.Data, "PrettyPrint", true));

            app.PlayButtonGenerateAudio.Value = false;
            app.PlayButtonGenerateAudio.Enable = "on";
            setStatusLampColor_tip(app, app.PlaybackLamp, "green", "Ready!");
        end

        % Button pushed function: SendtoCreateButton
        function SendtoCreateButtonPushed(app, event)
            app.SendtoCreateButton.Enable = "off";
            drawnow

            % Set the value of the params in the Create panel using value
            % from the Generate panel
            % Also select the correct Type, and only update relevant params

            app.FrequencyHzSpinner_2.Value = app.FrequencyHzSpinner.Value;
            
            app.DurationmsSpinner_2.Value = app.DurationmsSpinner.Value;
            app.AmplitudedBSpinner_2.Value = app.AmplitudedBSpinner.Value;
            app.SampleRateHzSpinner_2.Value = app.SampleRateHzSpinner.Value;
            app.EdgesmsSpinner_2.Value = app.EdgesmsSpinner.Value;
            

            if app.GenerateToneTypeButton.Value == 1
                % Set the Type in the Create tab to Tone
                app.CreateSweepTypeButton.Value = 0;
                app.CreateToneTypeButton.Value = 1;
    
                % Disable End Freq, Sweep Type options,
                % Also rename Start Frequency to just Frequency
                app.FrequencyHzLabel_2.Text = "Frequency (Hz)";
                app.EndFrequencyHzLabel_2.Enable = "off";
                app.EndFrequencyHzSpinner_2.Enable = "off";
                app.SweepFunctionLabel_2.Enable = "off";
                app.SweepFnDropDown_2.Enable = "off";
            elseif app.GenerateSweepTypeButton.Value == 1
                % The two params unique to Sweep
                app.EndFrequencyHzSpinner_2.Value = app.EndFrequencyHzSpinner.Value;
                app.SweepFnDropDown_2.Value = app.SweepFnDropDown.Value;

                % Set the Type in the Create tab to Sweep
                app.CreateToneTypeButton.Value = 0;
                app.CreateSweepTypeButton.Value = 1;
    
                % Enable End Freq, Sweep Type options,
                % Also rename Frequency to Start Frequency
                app.FrequencyHzLabel_2.Text = "Start Frequency (Hz)";
                app.EndFrequencyHzLabel_2.Enable = "on";
                app.EndFrequencyHzSpinner_2.Enable = "on";
                app.SweepFunctionLabel_2.Enable = "on";
                app.SweepFnDropDown_2.Enable = "on";
            end


            % Cosmetic: Change the ➥ icon (last character) of the button
            % Text to ✔
            app.SendtoCreateButton.Text = append(app.SendtoCreateButton.Text(1:end-1), '✔');

            % Shift the focused tab to Create
            tabHandle = app.TabGroup.Children(2);
            app.TabGroup.SelectedTab = tabHandle;

            
            app.SendtoCreateButton.Enable = "on";
        end

        % Value changed function: DownloadaCopyofThisPlaylistCheckBox
        function DownloadaCopyofThisPlaylistCheckBoxValueChanged(app, event)
            value = app.DownloadaCopyofThisPlaylistCheckBox.Value;
            
            % Change the content of the Create/Download button accordingly
            if value % with download
                app.CreateButtonGeneratePlaylist.Text = "📥︎  Create & Download Copy";
            else % no download, only Create
                app.CreateButtonGeneratePlaylist.Text = "✦  Create Playlist";
            end
        end

        % Value changed function: CreateButtonGeneratePlaylist
        function CreateButtonGeneratePlaylistValueChanged(app, event)
            app.CreateButtonGeneratePlaylist.Enable = "off";
            setStatusLampColor_tip(app, app.CreateLamp, "orange", "Creating a new random playlist...\n\nPlease select the save location when prompted.");
            drawnow

            file_count = app.CreateFileCountSpinner.Value;
            break_between_files = app.CreateInterstimulusIntervalmsSpinner.Value;
            withDownload = app.DownloadaCopyofThisPlaylistCheckBox.Value;

            if withDownload
                no_download = "false";
            else
                no_download = "true";
            end

            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/playlist/create', ...
                "?file_count=", num2str(file_count), "&break_between_files=", num2str(break_between_files), '&no_download=', no_download);
            
            response = app_HTTP_request(app, request, uri, app.CreateButtonGeneratePlaylist, app.CreateLamp, []);
            if isempty(response) || isfield(response, "error")
                return
            end

            % The server will need to do a reload of audio and playlists,
            % so pause for a bit to make sure it's finished the reload
            pause(1)

            % Handle response:
            % If withDownload AND has response txt data --> ask to save
            if withDownload && char(response.Header(2).Value) ~= "application/json" && endsWith(char(response.Header(2).Value), ".txt")
                fileName = char(response.Header(2).Value); % Get the default filename from the Header
                fileName = string(fileName(22:end)); % trim the tag in front: "attachment; filename=_____.txt"
                
                openDirTo = fullfile(app.LastState.SavePath, fileName);
                [file,path] = uiputfile(openDirTo,'Save Location');
                
                if ischar(file) && ischar(path)
                    filePath = fullfile(path, file);
                    fileID = fopen(filePath,'w');
                    fprintf(fileID, response.Body.Data);
                    fclose(fileID);
                    app.LastState.SavePath = path;
                end
            end

            if ~exist('fileName','var') == 1
                fileName = response.Body.Data.filename;
            end

            % Trigger the Playback Refresh button to get new state
            PlaybackRefreshListsButtonPushed(app, event)

            % Either go to Playback with this file, or Later (cancel)
            continue_decision = uiconfirm(app.AudioServerClientGUIUIFigure,sprintf(' ✎  %s\n\nThe new playlist has been created on the server!\n\nYou can now either go to Playback to try this out immediately, or you can do so later. If you decide to go to Playback now, the new playlist will be auto-selected for you ~',fileName),'New Random Playlist Created!', ...
                "Options",["Go to Playback", "Later"], ...
                "DefaultOption",1,"CancelOption",2);
        
            if continue_decision == "Go to Playback"
                % Select the From File panel
                app.PlaybackTypeSwitch.Value = "From Files";
                app.FromFilesPanel.Enable = "on";
                app.GeneratePanel.Enable = "off";

                % Select the Playlist filter
                app.FilterAudioFilesButton.Value = 0;
                app.FilterPlaylistsButton.Value = 1;
        
                % All random play is not available for Playlist
                allrandomCBValue = app.PlaythefilesAllRandomCheckBox.Value; % hold the checkbox value
                app.PlaythefilesAllRandomCheckBox.Value = 0;
                PlaythefilesAllRandomCheckBoxValueChanged(app, event); % reuse this function to handle the toggling of sub children
                app.PlaythefilesAllRandomCheckBox.Value = allrandomCBValue; % reset the value
                app.PlaythefilesAllRandomCheckBox.Visible = "off";

                % Filter function
    
                if isempty(app.PlaylistsList)
                    app.PlaybackFromFilesLogs.Value = sprintf("No Playlists available.");
                    return
                end
    
                % Filter for only Playlists and display on dropdown list
                % Update the current active Filter Dropdown
                app.FromFileDropDown.Items = app.PlaylistsList;
                if ~ismember(fileName, app.PlaylistsList)
                    fileName = app.PlaylistsList(1);
                end
                app.FromFileDropDown.Value = fileName;
                app.LastState.PlaybackPlaylistName = fileName;


                % Shift the focused tab to Create
                tabHandle = app.TabGroup.Children(1);
                app.TabGroup.SelectedTab = tabHandle;
            end

            app.CreateButtonGeneratePlaylist.Value = false;
            app.CreateButtonGeneratePlaylist.Enable = "on";
            setStatusLampColor_tip(app, app.CreateLamp, "green", "Ready!");
        end

        % Value changed function: CreateToneTypeButton
        function CreateToneTypeButtonValueChanged(app, event)
            if app.CreateSweepTypeButton.Value == 0
                app.CreateToneTypeButton.Value = 1;
                return
            end
            app.CreateSweepTypeButton.Value = 0;
            app.CreateToneTypeButton.Value = 1;

            % Disable End Freq, Sweep Type options,
            % Also rename Start Frequency to just Frequency
            app.FrequencyHzLabel_2.Text = "Frequency (Hz)";
            app.EndFrequencyHzLabel_2.Enable = "off";
            app.EndFrequencyHzSpinner_2.Enable = "off";
            app.SweepFunctionLabel_2.Enable = "off";
            app.SweepFnDropDown_2.Enable = "off";

            ToneSweepParamsValueChanged(app, event)
        end

        % Value changed function: CreateSweepTypeButton
        function CreateSweepTypeButtonValueChanged(app, event)
            if app.CreateToneTypeButton.Value == 0
                app.CreateSweepTypeButton.Value = 1;
                return
            end
            app.CreateToneTypeButton.Value = 0;
            app.CreateSweepTypeButton.Value = 1;

            % Enable End Freq, Sweep Type options,
            % Also rename Frequency to Start Frequency
            app.FrequencyHzLabel_2.Text = "Start Frequency (Hz)";
            app.EndFrequencyHzLabel_2.Enable = "on";
            app.EndFrequencyHzSpinner_2.Enable = "on";
            app.SweepFunctionLabel_2.Enable = "on";
            app.SweepFnDropDown_2.Enable = "on";

            ToneSweepParamsValueChanged(app, event)
        end

        % Value changed function: CreateButtonGenerateToneSweep
        function CreateButtonGenerateToneSweepValueChanged(app, event)
            app.CreateButtonGenerateToneSweep.Enable = "off";
            setStatusLampColor_tip(app, app.CreateLamp, "orange", "Making and Saving .wav file...\n\nPlease select the save location when prompted.");
            drawnow

            % make route from params
            if app.CreateToneTypeButton.Value == 1
                requestType = 'save_tone';
                data = strcat(num2str(app.FrequencyHzSpinner_2.Value), '/', num2str(app.DurationmsSpinner_2.Value), '/', ...
                    num2str(app.AmplitudedBSpinner_2.Value), '/', num2str(app.SampleRateHzSpinner_2.Value));
            elseif app.CreateSweepTypeButton.Value == 1
                requestType = 'save_sweep';
                data = strcat(lower(app.SweepFnDropDown_2.Value), '/', num2str(app.FrequencyHzSpinner_2.Value), '/', ...
                    num2str(app.EndFrequencyHzSpinner_2.Value), '/', num2str(app.DurationmsSpinner_2.Value), '/', ...
                    num2str(app.AmplitudedBSpinner_2.Value), '/', num2str(app.SampleRateHzSpinner_2.Value));
            end

            % Make sure that if the type is Sweep, the Edges must be a
            % negative number whose abs is <= floor(duration/2)
            if requestType == "save_sweep" && (app.EdgesmsSpinner_2.Value > 0 || abs(app.EdgesmsSpinner_2.Value) > floor(app.DurationmsSpinner_2.Value / 2))
                uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('For Sweep, the value of Edges must be negative (inclusive) AND its absolute value must be <= (Duration / 2). Please double-check the parameters and try again.'), ...
                    'Bad Parameters!', ...
                    "Options","Oops ~ Alright, I'll try again!", ...
                    "CancelOption",1, ...
                    "Icon","error");
                
                app.CreateButtonGenerateToneSweep.Value = false;
                app.CreateButtonGenerateToneSweep.Enable = "on";
                setStatusLampColor_tip(app, app.CreateLamp, "red", "Bad parameters. Please double-check and try again.");
                return
            elseif (app.EdgesmsSpinner_2.Value < 0 && abs(app.EdgesmsSpinner_2.Value) > floor(app.DurationmsSpinner_2.Value / 2))
                uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('For negative Edge, its absolute value must be <= (Duration / 2). Please double-check the parameters and try again.'), ...
                    'Bad Parameters!', ...
                    "Options","Oops ~ Alright, I'll try again!", ...
                    "CancelOption",1, ...
                    "Icon","error");
                app.CreateButtonGenerateToneSweep.Value = false;
                app.CreateButtonGenerateToneSweep.Enable = "on";
                setStatusLampColor_tip(app, app.CreateLamp, "red", "Bad parameters. Please double-check and try again.");
                return
            end

            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/', requestType, '/', data, '?edge=', num2str(app.EdgesmsSpinner_2.Value));
            drawnow
            
            response = app_HTTP_request(app, request, uri, app.CreateButtonGenerateToneSweep, app.CreateLamp, []);
            
            if isempty(response) || isfield(response, "error")
                return
            end

            if response.StatusCode ~= 200
                app.CreateButtonGenerateToneSweep.Value = false;
                app.CreateButtonGenerateToneSweep.Enable = "on";
                setStatusLampColor_tip(app, app.CreateLamp, "red", "The request was made but no audio was generated. Most likely the parameters are not correct or the audio server has crashed.\n\nIf you have access to the server computer, check the audio server log.");
            end

            fileName = char(response.Header(2).Value); % Get the default filename from the Header
            fileName = string(fileName(23:end-1)); % trim the tag in front: 'attachment; filename="440.0Hz_1000ms_60.0dB_@192000Hz.wav"'

            openDirTo = fullfile(app.LastState.SavePath, fileName);
            [file,path] = uiputfile(openDirTo,'Save Location');

            y = response.Body.Data(1); % this is parsed as a 1x1 cell array by matlab
            Fs = response.Body.Data(2); % this is parsed as a 1x1 cell array by matlab
            y = y{1}; % get the cell content
            Fs = Fs{1}; % get the cell contents
            
            if ischar(file) && ischar(path)
                filepath = fullfile(path, file);
                audiowrite(filepath,y,Fs);
                app.LastState.SavePath = path;
            end

            clear response y Fs

            app.CreateButtonGenerateToneSweep.Value = false;
            app.CreateButtonGenerateToneSweep.Enable = "on";
            setStatusLampColor_tip(app, app.CreateLamp, "green", "Ready!");
        end

        % Value changed function: DownloadaszipButton
        function DownloadaszipButtonValueChanged(app, event)
            app.DownloadaszipButton.Enable = "off";
            setStatusLampColor_tip(app, app.CreateLamp, "orange", "Saving batch files...\n\nPlease select the save location when prompted.");
            drawnow

            % determine the route from dropdown list
            dropdownValue = app.BatchFilesDropDown.Value;
            if dropdownValue == "Asynchronous Batch Files"
                route = "generate_batch_files_async";
            elseif dropdownValue == "Synchronous Batch Files"
                route = "generate_batch_files";
            end

            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/', route);
            response = app_HTTP_request(app, request, uri, app.DownloadaszipButton, app.CreateLamp, []);
            if isempty(response) || isfield(response, "error")
                return
            end

            if response.StatusCode == 404
                app.DownloadaszipButton.Value = false;
                app.DownloadaszipButton.Enable = "on";
                setStatusLampColor_tip(app, app.CreateLamp, "green", "Ready!");
                uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('The request is successful, but there is no audio file or playlist available. Nothing to download as it would be meaningless.'), ...
                    'No Audio File or Playlist Available!', ...
                    "Options","Got it!", ...
                    "CancelOption",1, ...
                    "Icon","warning");
                return
            end

            zipfileName = char(response.Header(2).Value); % Get the default filename from the Header
            zipfileName = string(zipfileName(22:end)); % trim the tag in front: "attachment; filename=_____.zip"

            openDirTo = fullfile(app.LastState.SavePath, zipfileName);
            [file,path] = uiputfile(openDirTo,'Save Location');

            if ischar(file) && ischar(path)
                zipPath = fullfile(path, file);
                fileID = fopen(zipPath,'w');
                fwrite(fileID, response.Body.Data);
                fclose(fileID);
                app.LastState.SavePath = path;
            end

            clear response

            app.DownloadaszipButton.Value = false;
            app.DownloadaszipButton.Enable = "on";
            setStatusLampColor_tip(app, app.CreateLamp, "green", "Ready!");
        end

        % Value changed function: InfoDropDown
        function InfoDropDownValueChanged(app, event)
            value = app.InfoDropDown.Value;
            if value == ""
                return
            end

            % Basic route: handle all /info/value
            % More complex stuff is posible when the audio server has them
            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/info' , '/', value);
            
            response = app_HTTP_request(app, request, uri, app.MainAPIDocumentationButton, [], app.InformationPanel);
            if isempty(response) || isfield(response, "error")
                return
            end

            % Handle error
            if response.StatusCode == 404
                app.InformationPanel.Value = "404: File not found";

                % Since the only way the user can choose this option is
                % from the current known list, if it fails, then most
                % likely the server's audio collection has changed
                % --> Ask to refresh
                refresh_decision = uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('This audio file or playlist is no longer exist or available on the server. You should refresh the current list now.'), ...
                    'Information Not Found', ...
                    "Options",["↺ Refresh List", "Later"], ...
                    "DefaultOption",1,"CancelOption",2, ...
                    "Icon","error");
                if refresh_decision == "↺ Refresh List"
                    PlaybackRefreshListsButtonPushed(app, event);

                    % reset the dropdown so that user has to click the
                    % filter option
                    app.InfoDropDown.Items = "";
                    app.InfoDropDown.Value = '';
                    app.InfoDropDown.Placeholder = "Relevant options will be shown here!";
                    app.InformationPanel.Value = "Requested information will be shown here!";
                end
                return
            elseif response.StatusCode ~= 200
                app.InformationPanel.Value = "Some error occurred, or no data found. The Command Window may report more information about this problem.";
                return
            end

            % Finally, update with the data
            app.InformationPanel.Value = response.Body.Data;
        end

        % Button pushed function: AudioFilesInfoButton
        function AudioFilesInfoButtonPushed(app, event)
            if ~isempty(app.AudioFilesList)
                app.InfoDropDown.Items = ["";app.AudioFilesList];
                app.InfoDropDown.Value = '';
                app.InfoDropDown.Placeholder = "Select an Audio File";
            else
                app.InfoDropDown.Items = "";
                app.InfoDropDown.Value = '';
                app.InfoDropDown.Placeholder = "No Audio File available!";
            end
        end

        % Button pushed function: PlaylistsInfoButton
        function PlaylistsInfoButtonPushed(app, event)
            if ~isempty(app.PlaylistsList)
                app.InfoDropDown.Items = ["";app.PlaylistsList];
                app.InfoDropDown.Value = '';
                app.InfoDropDown.Placeholder = "Select a Playlist File";
            else
                app.InfoDropDown.Items = "";
                app.InfoDropDown.Value = '';
                app.InfoDropDown.Placeholder = "No Playlist available!";
            end
        end

        % Button pushed function: MainAPIDocumentationButton
        function MainAPIDocumentationButtonPushed(app, event)
            app.MainAPIDocumentationButton.Enable = "off";
            drawnow

            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/');
            
            response = app_HTTP_request(app, request, uri, app.MainAPIDocumentationButton, [], app.InformationPanel);
            if isempty(response) || isfield(response, "error")
                return
            end

            app.InformationPanel.Value = response.Body.Data;

            app.MainAPIDocumentationButton.Enable = "on";
        end

        % Button pushed function: AvailableAudioFilesPlaylistsButton
        function AvailableAudioFilesPlaylistsButtonPushed(app, event)
            app.AvailableAudioFilesPlaylistsButton.Enable = "off";
            drawnow

            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), '/list');
            
            response = app_HTTP_request(app, request, uri, app.AvailableAudioFilesPlaylistsButton, [], app.InformationPanel);
            if isempty(response) || isfield(response, "error")
                return
            end

            app.InformationPanel.Value = response.Body.Data;

            app.AvailableAudioFilesPlaylistsButton.Enable = "on";
        end

        % Value changed function: ServerIPPortEditField
        function ServerIPPortEditFieldValueChanged(app, event)
            value = app.ServerIPPortEditField.Value;
            if ~startsWith(value, ["http://", "https://"])
                value = strcat('http://', value);
                app.ServerIPPortEditField.Value = value;
            end

            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), "/restart", '?restart=true');

            app.ManualRestartURI.Value = uri;

        end

        % Button pushed function: RestartButton
        function RestartButtonPushed(app, event)
            app.RestartButton.Enable = "off";
            drawnow
            request = matlab.net.http.RequestMessage;
            uri = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), "/restart", '?restart=true');

            response = app_HTTP_request(app, request, uri, app.RestartButton, [], []);
            if isempty(response) || isfield(response, "error")
                uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('Something went wrong while trying to send the restart request.\n\nIs the server online and reachable? If so, please check the output on the server console.\nYou may need to restart the server manually.'), ...
                    "Restart Request Error!", ...
                    "Options","OK", ...
                    "CancelOption",1, ...
                    "Icon","error");
                return
            end

            uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('The restart request is sent successfully. Typically, the server should be rebooted within 7 seconds. To check if the server is back, go to Playback > From Files and hit the Refresh button.'), ...
                    'Restart Status', ...
                    "Options","Got it!", ...
                    "CancelOption",1);

            app.RestartButton.Enable = "on";
        end

        % Button pushed function: ShutdownButton
        function ShutdownButtonPushed(app, event)
            app.ShutdownButton.Enable = "off";
            drawnow
            

            comfirm_decision = uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('Shutdown the audio server. Literally, shut it down. Gone.\n\nIf you do not have access to the server computer, you will NOT be able to start the audio server app back up.\n\nUnless you want to actually shutdown (close) the audio server app, consider using the Restart option instead.'),'Are you sure you want to shutdown the audio server app?', ...
                "Options",["Shut it down!", "Cancel"], ...
                "DefaultOption",2,"CancelOption",2, ...
                "Icon","warning");
        
            if comfirm_decision == "Cancel"
                app.ShutdownButton.Enable = "on";
                return
            end

            request = matlab.net.http.RequestMessage;
            % Request1 --> Get the shutdown token
            uri1 = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), "/shutdown", '?shutdown=YES_iamsureshutmedown');

            response1 = app_HTTP_request(app, request, uri1, app.ShutdownButton, [], []);
            if isempty(response1) || isfield(response1, "error")
                uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('Something went wrong while trying to send the shutdown request.\n[Fail to Get Shutdown Token]\n\nIs the server online and reachable? If so, please check the output on the server console.\nYou may need to shutdown the server manually.'), ...
                    'Shutdown Request Error!', ...
                    "Options","OK", ...
                    "CancelOption",1, ...
                    "Icon","error");
                return
            end

            token = response1.Body.Data.shutdown_token;

            % Request2 --> Shutdown Command
            uri2 = strcat(strip(app.ServerIPPortEditField.Value,'right','/'), "/shutdown", strcat('?token=', token));

            response2 = app_HTTP_request(app, request, uri2, app.ShutdownButton, [], []);
            if isempty(response2) || isfield(response2, "error")
                uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('Something went wrong while trying to send the shutdown request.\n[Fail to Send Shutdown Command]\n\nIs the server online and reachable? If so, please check the output on the server console.\nYou may need to shutdown the server manually."'), ...
                    'Shutdown Request Error!', ...
                    "Options","Got it!", ...
                    "CancelOption",1, ...
                    "Icon","error");
                return
            end

            uiconfirm(app.AudioServerClientGUIUIFigure,sprintf('The shutdown request is sent successfully. The audio server app should have shutdown gracefully.'), ...
                    'Shutdown Status', ...
                    "Options","Got it!", ...
                    "CancelOption",1);
            app.ShutdownButton.Enable = "on";
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create AudioServerClientGUIUIFigure and hide until all components are created
            app.AudioServerClientGUIUIFigure = uifigure('Visible', 'off');
            app.AudioServerClientGUIUIFigure.Color = [0.9412 0.9412 0.9412];
            app.AudioServerClientGUIUIFigure.Position = [100 100 960 680];
            app.AudioServerClientGUIUIFigure.Name = 'Audio Server | Client GUI';

            % Create TabGroup
            app.TabGroup = uitabgroup(app.AudioServerClientGUIUIFigure);
            app.TabGroup.Position = [0 0 960 680];

            % Create PlaybackTab
            app.PlaybackTab = uitab(app.TabGroup);
            app.PlaybackTab.Tooltip = {''};
            app.PlaybackTab.Title = 'Playback';

            % Create GridLayout7
            app.GridLayout7 = uigridlayout(app.PlaybackTab);
            app.GridLayout7.ColumnWidth = {'1.07x', 181.75, '1x', 'fit'};
            app.GridLayout7.RowHeight = {'1x', '1.2x', 'fit'};
            app.GridLayout7.RowSpacing = 6;
            app.GridLayout7.Padding = [10 7 10 7];

            % Create GeneratePanel
            app.GeneratePanel = uipanel(app.GridLayout7);
            app.GeneratePanel.Tooltip = {''};
            app.GeneratePanel.Enable = 'off';
            app.GeneratePanel.BorderWidth = 2;
            app.GeneratePanel.Title = '  Generate...';
            app.GeneratePanel.Layout.Row = 2;
            app.GeneratePanel.Layout.Column = [1 4];
            app.GeneratePanel.FontWeight = 'bold';
            app.GeneratePanel.FontSize = 14;

            % Create GridLayoutGenerate
            app.GridLayoutGenerate = uigridlayout(app.GeneratePanel);
            app.GridLayoutGenerate.ColumnWidth = {'1.4x', '1x', '1x', '0.05x', '1x', '1x', 'fit'};
            app.GridLayoutGenerate.RowHeight = {'fit', '1x', '1x', '1x', '1x', '1x', '1.7x'};

            % Create PlaybackGenerateAudioLog
            app.PlaybackGenerateAudioLog = uitextarea(app.GridLayoutGenerate);
            app.PlaybackGenerateAudioLog.Editable = 'off';
            app.PlaybackGenerateAudioLog.FontName = 'Cascadia Code';
            app.PlaybackGenerateAudioLog.FontSize = 10;
            app.PlaybackGenerateAudioLog.Placeholder = 'Latest HTTP response will be shown here...';
            app.PlaybackGenerateAudioLog.Layout.Row = 7;
            app.PlaybackGenerateAudioLog.Layout.Column = [1 7];

            % Create PlayButtonGenerateAudio
            app.PlayButtonGenerateAudio = uibutton(app.GridLayoutGenerate, 'state');
            app.PlayButtonGenerateAudio.ValueChangedFcn = createCallbackFcn(app, @PlayButtonGenerateAudioValueChanged, true);
            app.PlayButtonGenerateAudio.BusyAction = 'cancel';
            app.PlayButtonGenerateAudio.Tooltip = {'Send the request to the server to start playing the audio. You should not send any other request while the audio is playing.'; ''; 'While playing, the audio cannot be stopped until finished, unless the server is terminated.'};
            app.PlayButtonGenerateAudio.Text = '▷  Play';
            app.PlayButtonGenerateAudio.BackgroundColor = [0.8353 0.8863 0.9098];
            app.PlayButtonGenerateAudio.FontSize = 18;
            app.PlayButtonGenerateAudio.Layout.Row = 6;
            app.PlayButtonGenerateAudio.Layout.Column = [3 5];

            % Create SweepFnDropDown
            app.SweepFnDropDown = uidropdown(app.GridLayoutGenerate);
            app.SweepFnDropDown.Items = {'Linear', 'Quadratic', 'Logarithmic', 'Hyperbolic'};
            app.SweepFnDropDown.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.SweepFnDropDown.Enable = 'off';
            app.SweepFnDropDown.FontSize = 14;
            app.SweepFnDropDown.Layout.Row = 5;
            app.SweepFnDropDown.Layout.Column = [4 6];
            app.SweepFnDropDown.Value = 'Linear';

            % Create SweepFunctionLabel
            app.SweepFunctionLabel = uilabel(app.GridLayoutGenerate);
            app.SweepFunctionLabel.HorizontalAlignment = 'right';
            app.SweepFunctionLabel.FontSize = 14;
            app.SweepFunctionLabel.Enable = 'off';
            app.SweepFunctionLabel.Layout.Row = 5;
            app.SweepFunctionLabel.Layout.Column = [2 3];
            app.SweepFunctionLabel.Text = 'Sweep Function    ';

            % Create EdgesmsHelp
            app.EdgesmsHelp = uilabel(app.GridLayoutGenerate);
            app.EdgesmsHelp.HorizontalAlignment = 'center';
            app.EdgesmsHelp.FontSize = 18;
            app.EdgesmsHelp.FontWeight = 'bold';
            app.EdgesmsHelp.FontAngle = 'italic';
            app.EdgesmsHelp.FontColor = [0.3412 0.3412 0.3412];
            app.EdgesmsHelp.Tooltip = {'The rising and falling edges of the tone or sweep. In other words, how long for the audio to fade in and out.'; ''; 'A positive Edges value will add the rising and falling duration to the specified Duration. The actual duration of the audio would then be (Duration + 2 * Edges).'; ''; 'A negative Edges value will make the rising and falling duration inclusive. The specified Duration will remain unchanged. The duration the audio is played at the specified Amplitude would then be (Duration - 2 * Edges).'; ''; 'If Edges is negative, the absolute value of Edges must be less than or equal to (Duration / 2).'; ''; 'The amplitude ramp for rising and falling is linear on the linear amplitude scale (0-1).'; ''; ''; 'Set Edges = 0 to play without fading in and out.'};
            app.EdgesmsHelp.Layout.Row = 4;
            app.EdgesmsHelp.Layout.Column = 7;
            app.EdgesmsHelp.Text = '! ';

            % Create DurationmsSpinnerLabel
            app.DurationmsSpinnerLabel = uilabel(app.GridLayoutGenerate);
            app.DurationmsSpinnerLabel.HorizontalAlignment = 'right';
            app.DurationmsSpinnerLabel.FontSize = 14;
            app.DurationmsSpinnerLabel.Layout.Row = 3;
            app.DurationmsSpinnerLabel.Layout.Column = 2;
            app.DurationmsSpinnerLabel.Text = 'Duration (ms)';

            % Create AmplitudedBSpinnerLabel
            app.AmplitudedBSpinnerLabel = uilabel(app.GridLayoutGenerate);
            app.AmplitudedBSpinnerLabel.HorizontalAlignment = 'right';
            app.AmplitudedBSpinnerLabel.FontSize = 14;
            app.AmplitudedBSpinnerLabel.Layout.Row = 3;
            app.AmplitudedBSpinnerLabel.Layout.Column = 5;
            app.AmplitudedBSpinnerLabel.Text = 'Amplitude (dB)';

            % Create SampleRateHzSpinnerLabel
            app.SampleRateHzSpinnerLabel = uilabel(app.GridLayoutGenerate);
            app.SampleRateHzSpinnerLabel.HorizontalAlignment = 'right';
            app.SampleRateHzSpinnerLabel.FontSize = 14;
            app.SampleRateHzSpinnerLabel.Layout.Row = 4;
            app.SampleRateHzSpinnerLabel.Layout.Column = 2;
            app.SampleRateHzSpinnerLabel.Text = 'Sample Rate (Hz)';

            % Create EdgesmsSpinnerLabel
            app.EdgesmsSpinnerLabel = uilabel(app.GridLayoutGenerate);
            app.EdgesmsSpinnerLabel.HorizontalAlignment = 'right';
            app.EdgesmsSpinnerLabel.FontSize = 14;
            app.EdgesmsSpinnerLabel.Layout.Row = 4;
            app.EdgesmsSpinnerLabel.Layout.Column = 5;
            app.EdgesmsSpinnerLabel.Text = 'Edges (ms)';

            % Create EdgesmsSpinner
            app.EdgesmsSpinner = uispinner(app.GridLayoutGenerate);
            app.EdgesmsSpinner.RoundFractionalValues = 'on';
            app.EdgesmsSpinner.ValueDisplayFormat = '%.0f';
            app.EdgesmsSpinner.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.EdgesmsSpinner.FontSize = 14;
            app.EdgesmsSpinner.Tooltip = {'The rising and falling edges of the tone or sweep. In other words, how long for the audio to fade in and out.'; ''; 'A positive Edges value will add the rising and falling duration to the specified Duration. The actual duration of the audio would then be (Duration + 2 * Edges).'; ''; 'A negative Edges value will make the rising and falling duration inclusive. The specified Duration will remain unchanged. The duration the audio is played at the specified Amplitude would then be (Duration - 2 * Edges).'; ''; 'If Edges is negative, the absolute value of Edges must be less than or equal to (Duration / 2).'; ''; 'The amplitude ramp for rising and falling is linear on the linear amplitude scale (0-1).'; ''; ''; 'Set Edges = 0 to play without fading in and out.'};
            app.EdgesmsSpinner.Placeholder = 'Must be an integer, negative or positive.';
            app.EdgesmsSpinner.Layout.Row = 4;
            app.EdgesmsSpinner.Layout.Column = 6;

            % Create SampleRateHzSpinner
            app.SampleRateHzSpinner = uispinner(app.GridLayoutGenerate);
            app.SampleRateHzSpinner.Step = 4000;
            app.SampleRateHzSpinner.Limits = [4000 1000000];
            app.SampleRateHzSpinner.RoundFractionalValues = 'on';
            app.SampleRateHzSpinner.ValueDisplayFormat = '%.0f';
            app.SampleRateHzSpinner.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.SampleRateHzSpinner.FontSize = 14;
            app.SampleRateHzSpinner.Placeholder = 'Must be a positive integer.';
            app.SampleRateHzSpinner.Layout.Row = 4;
            app.SampleRateHzSpinner.Layout.Column = 3;
            app.SampleRateHzSpinner.Value = 192000;

            % Create AmplitudedBSpinner
            app.AmplitudedBSpinner = uispinner(app.GridLayoutGenerate);
            app.AmplitudedBSpinner.Limits = [-300 300];
            app.AmplitudedBSpinner.ValueDisplayFormat = '%.3f';
            app.AmplitudedBSpinner.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.AmplitudedBSpinner.FontSize = 14;
            app.AmplitudedBSpinner.Layout.Row = 3;
            app.AmplitudedBSpinner.Layout.Column = 6;
            app.AmplitudedBSpinner.Value = 60;

            % Create DurationmsSpinner
            app.DurationmsSpinner = uispinner(app.GridLayoutGenerate);
            app.DurationmsSpinner.Step = 100;
            app.DurationmsSpinner.Limits = [1 Inf];
            app.DurationmsSpinner.RoundFractionalValues = 'on';
            app.DurationmsSpinner.ValueDisplayFormat = '%.0f';
            app.DurationmsSpinner.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.DurationmsSpinner.FontSize = 14;
            app.DurationmsSpinner.Placeholder = 'Must be a positive integer.';
            app.DurationmsSpinner.Layout.Row = 3;
            app.DurationmsSpinner.Layout.Column = 3;
            app.DurationmsSpinner.Value = 1000;

            % Create EndFrequencyHzSpinner
            app.EndFrequencyHzSpinner = uispinner(app.GridLayoutGenerate);
            app.EndFrequencyHzSpinner.Step = 100;
            app.EndFrequencyHzSpinner.Limits = [0 250000];
            app.EndFrequencyHzSpinner.ValueDisplayFormat = '%.3f';
            app.EndFrequencyHzSpinner.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.EndFrequencyHzSpinner.FontSize = 14;
            app.EndFrequencyHzSpinner.Enable = 'off';
            app.EndFrequencyHzSpinner.Layout.Row = 2;
            app.EndFrequencyHzSpinner.Layout.Column = 6;
            app.EndFrequencyHzSpinner.Value = 14080;

            % Create EndFrequencyHzLabel
            app.EndFrequencyHzLabel = uilabel(app.GridLayoutGenerate);
            app.EndFrequencyHzLabel.HorizontalAlignment = 'right';
            app.EndFrequencyHzLabel.FontSize = 14;
            app.EndFrequencyHzLabel.Enable = 'off';
            app.EndFrequencyHzLabel.Layout.Row = 2;
            app.EndFrequencyHzLabel.Layout.Column = 5;
            app.EndFrequencyHzLabel.Text = 'End Frequency (Hz)';

            % Create FrequencyHzSpinner
            app.FrequencyHzSpinner = uispinner(app.GridLayoutGenerate);
            app.FrequencyHzSpinner.Step = 100;
            app.FrequencyHzSpinner.Limits = [0 250000];
            app.FrequencyHzSpinner.ValueDisplayFormat = '%.3f';
            app.FrequencyHzSpinner.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.FrequencyHzSpinner.FontSize = 14;
            app.FrequencyHzSpinner.Layout.Row = 2;
            app.FrequencyHzSpinner.Layout.Column = 3;
            app.FrequencyHzSpinner.Value = 440;

            % Create FrequencyHzLabel
            app.FrequencyHzLabel = uilabel(app.GridLayoutGenerate);
            app.FrequencyHzLabel.HorizontalAlignment = 'right';
            app.FrequencyHzLabel.FontSize = 14;
            app.FrequencyHzLabel.Layout.Row = 2;
            app.FrequencyHzLabel.Layout.Column = 2;
            app.FrequencyHzLabel.Text = 'Frequency (Hz)';

            % Create GenerateTypePanel
            app.GenerateTypePanel = uipanel(app.GridLayoutGenerate);
            app.GenerateTypePanel.BorderWidth = 2;
            app.GenerateTypePanel.Title = 'Type';
            app.GenerateTypePanel.Layout.Row = [1 6];
            app.GenerateTypePanel.Layout.Column = 1;
            app.GenerateTypePanel.FontWeight = 'bold';
            app.GenerateTypePanel.FontSize = 14;

            % Create GridLayoutGenerateType
            app.GridLayoutGenerateType = uigridlayout(app.GenerateTypePanel);

            % Create GenerateSweepTypeButton
            app.GenerateSweepTypeButton = uibutton(app.GridLayoutGenerateType, 'state');
            app.GenerateSweepTypeButton.ValueChangedFcn = createCallbackFcn(app, @GenerateSweepTypeButtonValueChanged, true);
            app.GenerateSweepTypeButton.Text = 'Sweep';
            app.GenerateSweepTypeButton.FontSize = 14;
            app.GenerateSweepTypeButton.Layout.Row = 2;
            app.GenerateSweepTypeButton.Layout.Column = [1 2];

            % Create GenerateToneTypeButton
            app.GenerateToneTypeButton = uibutton(app.GridLayoutGenerateType, 'state');
            app.GenerateToneTypeButton.ValueChangedFcn = createCallbackFcn(app, @GenerateToneTypeButtonValueChanged, true);
            app.GenerateToneTypeButton.Text = 'Sine Tone';
            app.GenerateToneTypeButton.FontSize = 14;
            app.GenerateToneTypeButton.Layout.Row = 1;
            app.GenerateToneTypeButton.Layout.Column = [1 2];
            app.GenerateToneTypeButton.Value = true;

            % Create GeneratePanelInfo
            app.GeneratePanelInfo = uilabel(app.GridLayoutGenerate);
            app.GeneratePanelInfo.HorizontalAlignment = 'center';
            app.GeneratePanelInfo.FontSize = 18;
            app.GeneratePanelInfo.FontWeight = 'bold';
            app.GeneratePanelInfo.FontAngle = 'italic';
            app.GeneratePanelInfo.Tooltip = {'Generate the pure tone or sweep and play it immediately.'; ''; 'The audio will be generated for every call, even if the same tone or sweep is requested multiple times. If performance and speed is a concern, Create the audio file first and play it directly.'};
            app.GeneratePanelInfo.Layout.Row = 1;
            app.GeneratePanelInfo.Layout.Column = 7;
            app.GeneratePanelInfo.Text = '? ';

            % Create SendtoCreateButton
            app.SendtoCreateButton = uibutton(app.GridLayoutGenerate, 'push');
            app.SendtoCreateButton.ButtonPushedFcn = createCallbackFcn(app, @SendtoCreateButtonPushed, true);
            app.SendtoCreateButton.BackgroundColor = [0.8745 0.8549 0.8902];
            app.SendtoCreateButton.Tooltip = {'Like this tone or sweep? Save it as a .wav file for later use (or as a keepsake...).'; ''; 'Click this button to send the current parameters to the Create tab. All you have to do next is just hit the Create & Download button!'; ''; 'Only relavant parameters for the current Type will be send, just so it wouldn''t change unnecessary fields!'};
            app.SendtoCreateButton.Layout.Row = 6;
            app.SendtoCreateButton.Layout.Column = 6;
            app.SendtoCreateButton.Text = 'Send to Create  ✔';

            % Create FromFilesPanel
            app.FromFilesPanel = uipanel(app.GridLayout7);
            app.FromFilesPanel.BorderWidth = 2;
            app.FromFilesPanel.Title = '  From Files';
            app.FromFilesPanel.Layout.Row = 1;
            app.FromFilesPanel.Layout.Column = [1 4];
            app.FromFilesPanel.FontWeight = 'bold';
            app.FromFilesPanel.FontSize = 14;

            % Create GridLayoutFromFiles
            app.GridLayoutFromFiles = uigridlayout(app.FromFilesPanel);
            app.GridLayoutFromFiles.ColumnWidth = {'2.4x', '2.5x', '1.3x', '0.9x', '0.25x', '2.05x', '1.1x', 'fit'};
            app.GridLayoutFromFiles.RowHeight = {'fit', '1x', '1x', '1x', '1.25x'};

            % Create PlaybackFromFilesLogs
            app.PlaybackFromFilesLogs = uitextarea(app.GridLayoutFromFiles);
            app.PlaybackFromFilesLogs.Editable = 'off';
            app.PlaybackFromFilesLogs.FontName = 'Cascadia Code';
            app.PlaybackFromFilesLogs.FontSize = 10;
            app.PlaybackFromFilesLogs.Placeholder = 'Latest HTTP response will be shown here...';
            app.PlaybackFromFilesLogs.Layout.Row = 5;
            app.PlaybackFromFilesLogs.Layout.Column = [1 7];

            % Create PlayButtonFromFiles
            app.PlayButtonFromFiles = uibutton(app.GridLayoutFromFiles, 'state');
            app.PlayButtonFromFiles.ValueChangedFcn = createCallbackFcn(app, @PlayButtonFromFilesValueChanged, true);
            app.PlayButtonFromFiles.BusyAction = 'cancel';
            app.PlayButtonFromFiles.Tooltip = {'Send the request to the server to start playing the audio. You should not send any other request while the audio is playing.'; ''; 'While playing, the audio cannot be stopped until finished, unless the server is terminated.'};
            app.PlayButtonFromFiles.Text = '▷  Play';
            app.PlayButtonFromFiles.BackgroundColor = [0.8353 0.8863 0.9098];
            app.PlayButtonFromFiles.FontSize = 18;
            app.PlayButtonFromFiles.Layout.Row = 4;
            app.PlayButtonFromFiles.Layout.Column = [3 5];

            % Create GaplessPlaybackCheckBox
            app.GaplessPlaybackCheckBox = uicheckbox(app.GridLayoutFromFiles);
            app.GaplessPlaybackCheckBox.Enable = 'off';
            app.GaplessPlaybackCheckBox.Visible = 'off';
            app.GaplessPlaybackCheckBox.Tooltip = {'Work in progress'};
            app.GaplessPlaybackCheckBox.Text = ' Gapless Playback';
            app.GaplessPlaybackCheckBox.FontSize = 14;
            app.GaplessPlaybackCheckBox.Layout.Row = 4;
            app.GaplessPlaybackCheckBox.Layout.Column = 2;

            % Create FromFileInterstimulusIntervalmsSpinner
            app.FromFileInterstimulusIntervalmsSpinner = uispinner(app.GridLayoutFromFiles);
            app.FromFileInterstimulusIntervalmsSpinner.Limits = [0 Inf];
            app.FromFileInterstimulusIntervalmsSpinner.RoundFractionalValues = 'on';
            app.FromFileInterstimulusIntervalmsSpinner.ValueDisplayFormat = '%.0f';
            app.FromFileInterstimulusIntervalmsSpinner.FontSize = 14;
            app.FromFileInterstimulusIntervalmsSpinner.Visible = 'off';
            app.FromFileInterstimulusIntervalmsSpinner.Tooltip = {'How long to wait before playing the next file.'; ''; 'Also known as the Interstimulus Interval.'};
            app.FromFileInterstimulusIntervalmsSpinner.Layout.Row = 3;
            app.FromFileInterstimulusIntervalmsSpinner.Layout.Column = 7;
            app.FromFileInterstimulusIntervalmsSpinner.Value = 1000;

            % Create FromFilePauseBetweenFilesmsLabel
            app.FromFilePauseBetweenFilesmsLabel = uilabel(app.GridLayoutFromFiles);
            app.FromFilePauseBetweenFilesmsLabel.HorizontalAlignment = 'right';
            app.FromFilePauseBetweenFilesmsLabel.FontSize = 14;
            app.FromFilePauseBetweenFilesmsLabel.Visible = 'off';
            app.FromFilePauseBetweenFilesmsLabel.Tooltip = {'How long to wait before playing the next file.'; ''; 'Also known as the Interstimulus Interval.'};
            app.FromFilePauseBetweenFilesmsLabel.Layout.Row = 3;
            app.FromFilePauseBetweenFilesmsLabel.Layout.Column = 6;
            app.FromFilePauseBetweenFilesmsLabel.Text = 'Pause Between Files (ms)';

            % Create FromFileFileCountSpinner
            app.FromFileFileCountSpinner = uispinner(app.GridLayoutFromFiles);
            app.FromFileFileCountSpinner.Limits = [1 Inf];
            app.FromFileFileCountSpinner.RoundFractionalValues = 'on';
            app.FromFileFileCountSpinner.ValueDisplayFormat = '%.0f';
            app.FromFileFileCountSpinner.FontSize = 14;
            app.FromFileFileCountSpinner.Visible = 'off';
            app.FromFileFileCountSpinner.Tooltip = {'How many files to play. For example, if the value is 5, then any 5 random files will be played.'; ''; 'The randomization is non-removed and uniform: all files have the same chance to be chosen at any time. This means that there is a chance a single file will be played File Count number of times.'};
            app.FromFileFileCountSpinner.Layout.Row = 3;
            app.FromFileFileCountSpinner.Layout.Column = 4;
            app.FromFileFileCountSpinner.Value = 5;

            % Create FromFileFileCountLabel
            app.FromFileFileCountLabel = uilabel(app.GridLayoutFromFiles);
            app.FromFileFileCountLabel.HorizontalAlignment = 'right';
            app.FromFileFileCountLabel.FontSize = 14;
            app.FromFileFileCountLabel.Visible = 'off';
            app.FromFileFileCountLabel.Tooltip = {'How many files to play. For example, if the value is 5, then any 5 random files will be played.'; ''; 'The randomization is non-removed and uniform: all files have the same chance to be chosen at any time. This means that there is a chance a single file will be played File Count number of times.'};
            app.FromFileFileCountLabel.Layout.Row = 3;
            app.FromFileFileCountLabel.Layout.Column = 3;
            app.FromFileFileCountLabel.Text = 'File Count';

            % Create PlaythefilesAllRandomCheckBox
            app.PlaythefilesAllRandomCheckBox = uicheckbox(app.GridLayoutFromFiles);
            app.PlaythefilesAllRandomCheckBox.ValueChangedFcn = createCallbackFcn(app, @PlaythefilesAllRandomCheckBoxValueChanged, true);
            app.PlaythefilesAllRandomCheckBox.Text = ' Play the files All Random';
            app.PlaythefilesAllRandomCheckBox.FontSize = 14;
            app.PlaythefilesAllRandomCheckBox.Layout.Row = 3;
            app.PlaythefilesAllRandomCheckBox.Layout.Column = 2;

            % Create FromFileDropDown
            app.FromFileDropDown = uidropdown(app.GridLayoutFromFiles);
            app.FromFileDropDown.Items = {};
            app.FromFileDropDown.ValueChangedFcn = createCallbackFcn(app, @FromFileDropDownValueChanged, true);
            app.FromFileDropDown.FontSize = 15;
            app.FromFileDropDown.BackgroundColor = [0.9412 0.9412 0.9412];
            app.FromFileDropDown.Placeholder = 'Make sure the audio server is on, then hit Refresh to update this list.';
            app.FromFileDropDown.Layout.Row = 2;
            app.FromFileDropDown.Layout.Column = [2 6];
            app.FromFileDropDown.Value = {};

            % Create FilterPanel
            app.FilterPanel = uipanel(app.GridLayoutFromFiles);
            app.FilterPanel.BorderWidth = 2;
            app.FilterPanel.Title = 'Filter...';
            app.FilterPanel.Layout.Row = [2 4];
            app.FilterPanel.Layout.Column = 1;
            app.FilterPanel.FontWeight = 'bold';
            app.FilterPanel.FontSize = 14;

            % Create GridLayoutPlaybackFilter
            app.GridLayoutPlaybackFilter = uigridlayout(app.FilterPanel);

            % Create FilterPlaylistsButton
            app.FilterPlaylistsButton = uibutton(app.GridLayoutPlaybackFilter, 'state');
            app.FilterPlaylistsButton.ValueChangedFcn = createCallbackFcn(app, @FilterPlaylistsButtonValueChanged, true);
            app.FilterPlaylistsButton.Text = 'Playlists';
            app.FilterPlaylistsButton.FontSize = 14;
            app.FilterPlaylistsButton.Layout.Row = 2;
            app.FilterPlaylistsButton.Layout.Column = [1 2];

            % Create FilterAudioFilesButton
            app.FilterAudioFilesButton = uibutton(app.GridLayoutPlaybackFilter, 'state');
            app.FilterAudioFilesButton.ValueChangedFcn = createCallbackFcn(app, @FilterAudioFilesButtonValueChanged, true);
            app.FilterAudioFilesButton.Text = 'Audio Files';
            app.FilterAudioFilesButton.FontSize = 14;
            app.FilterAudioFilesButton.Layout.Row = 1;
            app.FilterAudioFilesButton.Layout.Column = [1 2];
            app.FilterAudioFilesButton.Value = true;

            % Create PlaybackRefreshListsButton
            app.PlaybackRefreshListsButton = uibutton(app.GridLayoutFromFiles, 'push');
            app.PlaybackRefreshListsButton.ButtonPushedFcn = createCallbackFcn(app, @PlaybackRefreshListsButtonPushed, true);
            app.PlaybackRefreshListsButton.BackgroundColor = [0.9294 0.9216 0.8745];
            app.PlaybackRefreshListsButton.FontWeight = 'bold';
            app.PlaybackRefreshListsButton.Layout.Row = 1;
            app.PlaybackRefreshListsButton.Layout.Column = 1;
            app.PlaybackRefreshListsButton.Text = '↺  Refresh Lists';

            % Create FromFilesPanelInfo
            app.FromFilesPanelInfo = uilabel(app.GridLayoutFromFiles);
            app.FromFilesPanelInfo.HorizontalAlignment = 'center';
            app.FromFilesPanelInfo.FontSize = 18;
            app.FromFilesPanelInfo.FontWeight = 'bold';
            app.FromFilesPanelInfo.FontAngle = 'italic';
            app.FromFilesPanelInfo.Tooltip = {'Play available audio files (.wav, .flac, .mp3,...) or playlists (.txt) on the server.'; ''; 'The available options are shown in the dropdown list. To view the comprehensive list of available audio files and playlists, go to the Information tab.'};
            app.FromFilesPanelInfo.Layout.Row = 1;
            app.FromFilesPanelInfo.Layout.Column = 8;
            app.FromFilesPanelInfo.Text = '? ';

            % Create SeeInfoButton
            app.SeeInfoButton = uibutton(app.GridLayoutFromFiles, 'push');
            app.SeeInfoButton.ButtonPushedFcn = createCallbackFcn(app, @SeeInfoButtonPushed, true);
            app.SeeInfoButton.BackgroundColor = [0.9216 0.9059 0.8941];
            app.SeeInfoButton.FontAngle = 'italic';
            app.SeeInfoButton.Tooltip = {'Click to go to the Information tab to see this file''s information / metadata.'};
            app.SeeInfoButton.Layout.Row = 2;
            app.SeeInfoButton.Layout.Column = 7;
            app.SeeInfoButton.Text = 'See Info';

            % Create PlaybackTypeSwitch
            app.PlaybackTypeSwitch = uiswitch(app.GridLayout7, 'slider');
            app.PlaybackTypeSwitch.Items = {'From Files', 'Generate'};
            app.PlaybackTypeSwitch.ValueChangedFcn = createCallbackFcn(app, @PlaybackTypeSwitchValueChanged, true);
            app.PlaybackTypeSwitch.FontSize = 14;
            app.PlaybackTypeSwitch.FontAngle = 'italic';
            app.PlaybackTypeSwitch.Layout.Row = 3;
            app.PlaybackTypeSwitch.Layout.Column = 2;
            app.PlaybackTypeSwitch.Value = 'From Files';

            % Create PlaybackLamp
            app.PlaybackLamp = uilamp(app.GridLayout7);
            app.PlaybackLamp.Tooltip = {'Ready!'};
            app.PlaybackLamp.Layout.Row = 3;
            app.PlaybackLamp.Layout.Column = 4;
            app.PlaybackLamp.Color = [0.7412 0.851 0.6902];

            % Create CreateTab
            app.CreateTab = uitab(app.TabGroup);
            app.CreateTab.Title = 'Create';

            % Create GridLayout2
            app.GridLayout2 = uigridlayout(app.CreateTab);
            app.GridLayout2.ColumnWidth = {'1x', 'fit'};
            app.GridLayout2.RowHeight = {'1x', '1.46x', '0.37x', 'fit'};
            app.GridLayout2.RowSpacing = 6;
            app.GridLayout2.Padding = [10 7 10 7];

            % Create WindowsBatchFilesPanel
            app.WindowsBatchFilesPanel = uipanel(app.GridLayout2);
            app.WindowsBatchFilesPanel.BorderWidth = 2;
            app.WindowsBatchFilesPanel.Title = 'Windows Batch Files';
            app.WindowsBatchFilesPanel.Layout.Row = 3;
            app.WindowsBatchFilesPanel.Layout.Column = [1 2];
            app.WindowsBatchFilesPanel.FontWeight = 'bold';
            app.WindowsBatchFilesPanel.FontSize = 14;

            % Create GridLayout5
            app.GridLayout5 = uigridlayout(app.WindowsBatchFilesPanel);
            app.GridLayout5.ColumnWidth = {'1x', '0.5x', 'fit'};
            app.GridLayout5.RowHeight = {'1x'};

            % Create BatchFilesDropDown
            app.BatchFilesDropDown = uidropdown(app.GridLayout5);
            app.BatchFilesDropDown.Items = {'Asynchronous Batch Files', 'Synchronous Batch Files'};
            app.BatchFilesDropDown.Tooltip = {'Select which type of .bat files you need.'; ''; '- Synchronous .bat files work using the Windows'' built-in function "curl" in the command line to send the API requests. This type of .bat file waits for the server to respond, and then returns the message sent back by the server. This will block the terminal or other process until the job is finished server-side, say a playlist has finished playing. While this option provides the information about your API call, the "blocking" nature is unsuited for many use cases. If you want to send the API request and immediately do something else, use the Asynchronous option.'; ''; '- Asynchronous .bat files use a custom script "async_get.exe" to send the API requests. Under the hood, "async_get.exe" forwards the API call to a background process, then immediately exit. This way, the request is still made, but the initial .bat script is non-blocking. Asynchronous .bat files are better suited if you trigger them as a part of some bigger scripts or processes. If you need to know the status of your requests or you need to wait until the server-side job is complete before moving forward, use the Synchronous option.'};
            app.BatchFilesDropDown.FontSize = 14;
            app.BatchFilesDropDown.Layout.Row = 1;
            app.BatchFilesDropDown.Layout.Column = 1;
            app.BatchFilesDropDown.Value = 'Asynchronous Batch Files';

            % Create BatchFilesInfo
            app.BatchFilesInfo = uilabel(app.GridLayout5);
            app.BatchFilesInfo.HorizontalAlignment = 'center';
            app.BatchFilesInfo.FontSize = 18;
            app.BatchFilesInfo.FontWeight = 'bold';
            app.BatchFilesInfo.FontAngle = 'italic';
            app.BatchFilesInfo.Tooltip = {'Download .bat files that start the audio for each audio files and playlists.'; ''; 'Two different ways to make the API calls are available. See the detail tooltip by hovering on the drop-down list.'; ''; 'Select your option, then click Download. You will be prompted to select your download location. The result is a .zip file with all of the batch files and necessary scripts.'};
            app.BatchFilesInfo.Layout.Row = 1;
            app.BatchFilesInfo.Layout.Column = 3;
            app.BatchFilesInfo.Text = ' ? ';

            % Create DownloadaszipButton
            app.DownloadaszipButton = uibutton(app.GridLayout5, 'state');
            app.DownloadaszipButton.ValueChangedFcn = createCallbackFcn(app, @DownloadaszipButtonValueChanged, true);
            app.DownloadaszipButton.Tooltip = {'You will be prompted to select the download location. Afterwards, extract the .zip file into a folder.'; ''; 'You may need to "Unblock" the .zip file before extracting if Windows throws a complain when you run the .bat file:'; ''; 'Right-click the .zip file > Properties > Unblock (the check box in the lower-right) > Apply'};
            app.DownloadaszipButton.Text = '📥︎  Download as .zip';
            app.DownloadaszipButton.BackgroundColor = [0.7569 0.8706 0.8157];
            app.DownloadaszipButton.FontSize = 14;
            app.DownloadaszipButton.FontWeight = 'bold';
            app.DownloadaszipButton.Layout.Row = 1;
            app.DownloadaszipButton.Layout.Column = 2;

            % Create ToneSweepPanel
            app.ToneSweepPanel = uipanel(app.GridLayout2);
            app.ToneSweepPanel.BorderWidth = 2;
            app.ToneSweepPanel.Title = 'Tone & Sweep';
            app.ToneSweepPanel.Layout.Row = 2;
            app.ToneSweepPanel.Layout.Column = [1 2];
            app.ToneSweepPanel.FontWeight = 'bold';
            app.ToneSweepPanel.FontSize = 14;

            % Create GridLayoutCreateToneSweep
            app.GridLayoutCreateToneSweep = uigridlayout(app.ToneSweepPanel);
            app.GridLayoutCreateToneSweep.ColumnWidth = {'1.4x', '1x', '1x', '0.05x', '1x', '1x', 'fit'};
            app.GridLayoutCreateToneSweep.RowHeight = {'0.3x', '1x', '1x', '1x', '1x', '0.1x', 'fit'};

            % Create CreateButtonGenerateToneSweep
            app.CreateButtonGenerateToneSweep = uibutton(app.GridLayoutCreateToneSweep, 'state');
            app.CreateButtonGenerateToneSweep.ValueChangedFcn = createCallbackFcn(app, @CreateButtonGenerateToneSweepValueChanged, true);
            app.CreateButtonGenerateToneSweep.BusyAction = 'cancel';
            app.CreateButtonGenerateToneSweep.Tooltip = {'You will be prompted to select the download location after clicking this button.'};
            app.CreateButtonGenerateToneSweep.Text = '📥︎  Create & Download';
            app.CreateButtonGenerateToneSweep.BackgroundColor = [0.9098 0.8784 0.8353];
            app.CreateButtonGenerateToneSweep.FontSize = 18;
            app.CreateButtonGenerateToneSweep.Layout.Row = 7;
            app.CreateButtonGenerateToneSweep.Layout.Column = [2 6];

            % Create SweepFnDropDown_2
            app.SweepFnDropDown_2 = uidropdown(app.GridLayoutCreateToneSweep);
            app.SweepFnDropDown_2.Items = {'Linear', 'Quadratic', 'Logarithmic', 'Hyperbolic'};
            app.SweepFnDropDown_2.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.SweepFnDropDown_2.Enable = 'off';
            app.SweepFnDropDown_2.FontSize = 14;
            app.SweepFnDropDown_2.Layout.Row = 5;
            app.SweepFnDropDown_2.Layout.Column = [4 6];
            app.SweepFnDropDown_2.Value = 'Linear';

            % Create SweepFunctionLabel_2
            app.SweepFunctionLabel_2 = uilabel(app.GridLayoutCreateToneSweep);
            app.SweepFunctionLabel_2.HorizontalAlignment = 'right';
            app.SweepFunctionLabel_2.FontSize = 14;
            app.SweepFunctionLabel_2.Enable = 'off';
            app.SweepFunctionLabel_2.Layout.Row = 5;
            app.SweepFunctionLabel_2.Layout.Column = [2 3];
            app.SweepFunctionLabel_2.Text = 'Sweep Function    ';

            % Create EdgesmsHelp_2
            app.EdgesmsHelp_2 = uilabel(app.GridLayoutCreateToneSweep);
            app.EdgesmsHelp_2.HorizontalAlignment = 'center';
            app.EdgesmsHelp_2.FontSize = 18;
            app.EdgesmsHelp_2.FontWeight = 'bold';
            app.EdgesmsHelp_2.FontAngle = 'italic';
            app.EdgesmsHelp_2.FontColor = [0.3412 0.3412 0.3412];
            app.EdgesmsHelp_2.Tooltip = {'The rising and falling edges of the tone or sweep. In other words, how long for the audio to fade in and out.'; ''; 'A positive Edges value will add the rising and falling duration to the specified Duration. The actual duration of the audio would then be (Duration + 2 * Edges).'; ''; 'A negative Edges value will make the rising and falling duration inclusive. The specified Duration will remain unchanged. The duration the audio is played at the specified Amplitude would then be (Duration - 2 * Edges).'; ''; 'If Edges is negative, the absolute value of Edges must be less than or equal to (Duration / 2).'; ''; 'The amplitude ramp for rising and falling is linear on the linear amplitude scale (0-1).'; ''; ''; 'Set Edges = 0 to play without fading in and out.'};
            app.EdgesmsHelp_2.Layout.Row = 4;
            app.EdgesmsHelp_2.Layout.Column = 7;
            app.EdgesmsHelp_2.Text = '! ';

            % Create EdgesmsSpinner_2
            app.EdgesmsSpinner_2 = uispinner(app.GridLayoutCreateToneSweep);
            app.EdgesmsSpinner_2.RoundFractionalValues = 'on';
            app.EdgesmsSpinner_2.ValueDisplayFormat = '%.0f';
            app.EdgesmsSpinner_2.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.EdgesmsSpinner_2.FontSize = 14;
            app.EdgesmsSpinner_2.Tooltip = {'The rising and falling edges of the tone or sweep. In other words, how long for the audio to fade in and out.'; ''; 'A positive Edges value will add the rising and falling duration to the specified Duration. The actual duration of the audio would then be (Duration + 2 * Edges).'; ''; 'A negative Edges value will make the rising and falling duration inclusive. The specified Duration will remain unchanged. The duration the audio is played at the specified Amplitude would then be (Duration - 2 * Edges).'; ''; 'If Edges is negative, the absolute value of Edges must be less than or equal to (Duration / 2).'; ''; 'The amplitude ramp for rising and falling is linear on the linear amplitude scale (0-1).'; ''; ''; 'Set Edges = 0 to play without fading in and out.'};
            app.EdgesmsSpinner_2.Placeholder = 'Must be an integer, negative or positive.';
            app.EdgesmsSpinner_2.Layout.Row = 4;
            app.EdgesmsSpinner_2.Layout.Column = 6;

            % Create SampleRateHzSpinner_2
            app.SampleRateHzSpinner_2 = uispinner(app.GridLayoutCreateToneSweep);
            app.SampleRateHzSpinner_2.Step = 4000;
            app.SampleRateHzSpinner_2.Limits = [4000 1000000];
            app.SampleRateHzSpinner_2.RoundFractionalValues = 'on';
            app.SampleRateHzSpinner_2.ValueDisplayFormat = '%.0f';
            app.SampleRateHzSpinner_2.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.SampleRateHzSpinner_2.FontSize = 14;
            app.SampleRateHzSpinner_2.Placeholder = 'Must be a positive integer.';
            app.SampleRateHzSpinner_2.Layout.Row = 4;
            app.SampleRateHzSpinner_2.Layout.Column = 3;
            app.SampleRateHzSpinner_2.Value = 192000;

            % Create AmplitudedBSpinner_2
            app.AmplitudedBSpinner_2 = uispinner(app.GridLayoutCreateToneSweep);
            app.AmplitudedBSpinner_2.Limits = [-300 300];
            app.AmplitudedBSpinner_2.ValueDisplayFormat = '%.3f';
            app.AmplitudedBSpinner_2.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.AmplitudedBSpinner_2.FontSize = 14;
            app.AmplitudedBSpinner_2.Layout.Row = 3;
            app.AmplitudedBSpinner_2.Layout.Column = 6;
            app.AmplitudedBSpinner_2.Value = 60;

            % Create DurationmsSpinner_2Label
            app.DurationmsSpinner_2Label = uilabel(app.GridLayoutCreateToneSweep);
            app.DurationmsSpinner_2Label.HorizontalAlignment = 'right';
            app.DurationmsSpinner_2Label.FontSize = 14;
            app.DurationmsSpinner_2Label.Layout.Row = 3;
            app.DurationmsSpinner_2Label.Layout.Column = 2;
            app.DurationmsSpinner_2Label.Text = 'Duration (ms)';

            % Create DurationmsSpinner_2
            app.DurationmsSpinner_2 = uispinner(app.GridLayoutCreateToneSweep);
            app.DurationmsSpinner_2.Step = 100;
            app.DurationmsSpinner_2.Limits = [1 Inf];
            app.DurationmsSpinner_2.RoundFractionalValues = 'on';
            app.DurationmsSpinner_2.ValueDisplayFormat = '%.0f';
            app.DurationmsSpinner_2.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.DurationmsSpinner_2.FontSize = 14;
            app.DurationmsSpinner_2.Placeholder = 'Must be a positive integer.';
            app.DurationmsSpinner_2.Layout.Row = 3;
            app.DurationmsSpinner_2.Layout.Column = 3;
            app.DurationmsSpinner_2.Value = 1000;

            % Create AmplitudedBSpinner_2Label
            app.AmplitudedBSpinner_2Label = uilabel(app.GridLayoutCreateToneSweep);
            app.AmplitudedBSpinner_2Label.HorizontalAlignment = 'right';
            app.AmplitudedBSpinner_2Label.FontSize = 14;
            app.AmplitudedBSpinner_2Label.Layout.Row = 3;
            app.AmplitudedBSpinner_2Label.Layout.Column = 5;
            app.AmplitudedBSpinner_2Label.Text = 'Amplitude (dB)';

            % Create SampleRateHzSpinner_2Label
            app.SampleRateHzSpinner_2Label = uilabel(app.GridLayoutCreateToneSweep);
            app.SampleRateHzSpinner_2Label.HorizontalAlignment = 'right';
            app.SampleRateHzSpinner_2Label.FontSize = 14;
            app.SampleRateHzSpinner_2Label.Layout.Row = 4;
            app.SampleRateHzSpinner_2Label.Layout.Column = 2;
            app.SampleRateHzSpinner_2Label.Text = 'Sample Rate (Hz)';

            % Create EdgesmsSpinner_2Label
            app.EdgesmsSpinner_2Label = uilabel(app.GridLayoutCreateToneSweep);
            app.EdgesmsSpinner_2Label.HorizontalAlignment = 'right';
            app.EdgesmsSpinner_2Label.FontSize = 14;
            app.EdgesmsSpinner_2Label.Layout.Row = 4;
            app.EdgesmsSpinner_2Label.Layout.Column = 5;
            app.EdgesmsSpinner_2Label.Text = 'Edges (ms)';

            % Create EndFrequencyHzSpinner_2
            app.EndFrequencyHzSpinner_2 = uispinner(app.GridLayoutCreateToneSweep);
            app.EndFrequencyHzSpinner_2.Step = 100;
            app.EndFrequencyHzSpinner_2.Limits = [0 250000];
            app.EndFrequencyHzSpinner_2.ValueDisplayFormat = '%.3f';
            app.EndFrequencyHzSpinner_2.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.EndFrequencyHzSpinner_2.FontSize = 14;
            app.EndFrequencyHzSpinner_2.Enable = 'off';
            app.EndFrequencyHzSpinner_2.Layout.Row = 2;
            app.EndFrequencyHzSpinner_2.Layout.Column = 6;
            app.EndFrequencyHzSpinner_2.Value = 14080;

            % Create EndFrequencyHzLabel_2
            app.EndFrequencyHzLabel_2 = uilabel(app.GridLayoutCreateToneSweep);
            app.EndFrequencyHzLabel_2.HorizontalAlignment = 'right';
            app.EndFrequencyHzLabel_2.FontSize = 14;
            app.EndFrequencyHzLabel_2.Enable = 'off';
            app.EndFrequencyHzLabel_2.Layout.Row = 2;
            app.EndFrequencyHzLabel_2.Layout.Column = 5;
            app.EndFrequencyHzLabel_2.Text = 'End Frequency (Hz)';

            % Create FrequencyHzSpinner_2
            app.FrequencyHzSpinner_2 = uispinner(app.GridLayoutCreateToneSweep);
            app.FrequencyHzSpinner_2.Step = 100;
            app.FrequencyHzSpinner_2.Limits = [0 250000];
            app.FrequencyHzSpinner_2.ValueDisplayFormat = '%.3f';
            app.FrequencyHzSpinner_2.ValueChangedFcn = createCallbackFcn(app, @ToneSweepParamsValueChanged, true);
            app.FrequencyHzSpinner_2.FontSize = 14;
            app.FrequencyHzSpinner_2.Layout.Row = 2;
            app.FrequencyHzSpinner_2.Layout.Column = 3;
            app.FrequencyHzSpinner_2.Value = 440;

            % Create FrequencyHzLabel_2
            app.FrequencyHzLabel_2 = uilabel(app.GridLayoutCreateToneSweep);
            app.FrequencyHzLabel_2.HorizontalAlignment = 'right';
            app.FrequencyHzLabel_2.FontSize = 14;
            app.FrequencyHzLabel_2.Layout.Row = 2;
            app.FrequencyHzLabel_2.Layout.Column = 2;
            app.FrequencyHzLabel_2.Text = 'Frequency (Hz)';

            % Create CreateTypeToneSweepPanel
            app.CreateTypeToneSweepPanel = uipanel(app.GridLayoutCreateToneSweep);
            app.CreateTypeToneSweepPanel.BorderWidth = 2;
            app.CreateTypeToneSweepPanel.Title = 'Type';
            app.CreateTypeToneSweepPanel.Layout.Row = [1 7];
            app.CreateTypeToneSweepPanel.Layout.Column = 1;
            app.CreateTypeToneSweepPanel.FontWeight = 'bold';
            app.CreateTypeToneSweepPanel.FontSize = 14;

            % Create GridLayoutCreateTypeToneSweep
            app.GridLayoutCreateTypeToneSweep = uigridlayout(app.CreateTypeToneSweepPanel);

            % Create CreateSweepTypeButton
            app.CreateSweepTypeButton = uibutton(app.GridLayoutCreateTypeToneSweep, 'state');
            app.CreateSweepTypeButton.ValueChangedFcn = createCallbackFcn(app, @CreateSweepTypeButtonValueChanged, true);
            app.CreateSweepTypeButton.Text = 'Sweep';
            app.CreateSweepTypeButton.FontSize = 14;
            app.CreateSweepTypeButton.Layout.Row = 2;
            app.CreateSweepTypeButton.Layout.Column = [1 2];

            % Create CreateToneTypeButton
            app.CreateToneTypeButton = uibutton(app.GridLayoutCreateTypeToneSweep, 'state');
            app.CreateToneTypeButton.ValueChangedFcn = createCallbackFcn(app, @CreateToneTypeButtonValueChanged, true);
            app.CreateToneTypeButton.Text = 'Sine Tone';
            app.CreateToneTypeButton.FontSize = 14;
            app.CreateToneTypeButton.Layout.Row = 1;
            app.CreateToneTypeButton.Layout.Column = [1 2];
            app.CreateToneTypeButton.Value = true;

            % Create CreateToneSweepInfo
            app.CreateToneSweepInfo = uilabel(app.GridLayoutCreateToneSweep);
            app.CreateToneSweepInfo.HorizontalAlignment = 'center';
            app.CreateToneSweepInfo.FontSize = 18;
            app.CreateToneSweepInfo.FontWeight = 'bold';
            app.CreateToneSweepInfo.FontAngle = 'italic';
            app.CreateToneSweepInfo.Tooltip = {'Create the pure tone or sweep as a .wav file to be downloaded.'; ''; 'You will be prompted to select the download location after clicking the Create & Download button.'};
            app.CreateToneSweepInfo.Layout.Row = 7;
            app.CreateToneSweepInfo.Layout.Column = 7;
            app.CreateToneSweepInfo.Text = '? ';

            % Create CreateRandomPlaylist
            app.CreateRandomPlaylist = uipanel(app.GridLayout2);
            app.CreateRandomPlaylist.BorderWidth = 2;
            app.CreateRandomPlaylist.Title = 'Random Playlist';
            app.CreateRandomPlaylist.Layout.Row = 1;
            app.CreateRandomPlaylist.Layout.Column = [1 2];
            app.CreateRandomPlaylist.FontWeight = 'bold';
            app.CreateRandomPlaylist.FontSize = 14;

            % Create GridLayout3
            app.GridLayout3 = uigridlayout(app.CreateRandomPlaylist);
            app.GridLayout3.ColumnWidth = {'1.022x', '0.8x', '1.25x', '1x', 'fit'};
            app.GridLayout3.RowHeight = {'1x', '1x', '1x', 'fit'};

            % Create CreateButtonGeneratePlaylist
            app.CreateButtonGeneratePlaylist = uibutton(app.GridLayout3, 'state');
            app.CreateButtonGeneratePlaylist.ValueChangedFcn = createCallbackFcn(app, @CreateButtonGeneratePlaylistValueChanged, true);
            app.CreateButtonGeneratePlaylist.BusyAction = 'cancel';
            app.CreateButtonGeneratePlaylist.Tooltip = {'Send the request to the server to make a new randomized playlist.'; ''; 'The new playlist is always saved on the server-side. If you also chose to Download a copy, you will be prompted to select a download location afterwards.'};
            app.CreateButtonGeneratePlaylist.Text = '✦  Create Playlist';
            app.CreateButtonGeneratePlaylist.BackgroundColor = [0.9412 0.9294 0.8941];
            app.CreateButtonGeneratePlaylist.FontSize = 18;
            app.CreateButtonGeneratePlaylist.Layout.Row = 4;
            app.CreateButtonGeneratePlaylist.Layout.Column = [2 4];

            % Create DownloadaCopyofThisPlaylistCheckBox
            app.DownloadaCopyofThisPlaylistCheckBox = uicheckbox(app.GridLayout3);
            app.DownloadaCopyofThisPlaylistCheckBox.ValueChangedFcn = createCallbackFcn(app, @DownloadaCopyofThisPlaylistCheckBoxValueChanged, true);
            app.DownloadaCopyofThisPlaylistCheckBox.Tooltip = {'The playlist will always be created on the server. However, a copy of the playlist can be retrieved now, just as a peace of mind.'; ''; 'Do you want a receipt?'};
            app.DownloadaCopyofThisPlaylistCheckBox.Text = '   Also Download a Copy of This Playlist';
            app.DownloadaCopyofThisPlaylistCheckBox.FontSize = 16;
            app.DownloadaCopyofThisPlaylistCheckBox.Layout.Row = 3;
            app.DownloadaCopyofThisPlaylistCheckBox.Layout.Column = [2 3];

            % Create CreateInterstimulusIntervalmsSpinner
            app.CreateInterstimulusIntervalmsSpinner = uispinner(app.GridLayout3);
            app.CreateInterstimulusIntervalmsSpinner.Limits = [0 Inf];
            app.CreateInterstimulusIntervalmsSpinner.RoundFractionalValues = 'on';
            app.CreateInterstimulusIntervalmsSpinner.ValueDisplayFormat = '%.0f';
            app.CreateInterstimulusIntervalmsSpinner.FontSize = 16;
            app.CreateInterstimulusIntervalmsSpinner.Tooltip = {'How long to wait before playing the next file.'; ''; 'Also known as the Interstimulus Interval.'};
            app.CreateInterstimulusIntervalmsSpinner.Layout.Row = 2;
            app.CreateInterstimulusIntervalmsSpinner.Layout.Column = 4;
            app.CreateInterstimulusIntervalmsSpinner.Value = 1000;

            % Create CreatePauseBetweenFilesmsLabel
            app.CreatePauseBetweenFilesmsLabel = uilabel(app.GridLayout3);
            app.CreatePauseBetweenFilesmsLabel.HorizontalAlignment = 'right';
            app.CreatePauseBetweenFilesmsLabel.FontSize = 16;
            app.CreatePauseBetweenFilesmsLabel.Tooltip = {'How long to wait before playing the next file.'; ''; 'Also known as the Interstimulus Interval.'};
            app.CreatePauseBetweenFilesmsLabel.Layout.Row = 2;
            app.CreatePauseBetweenFilesmsLabel.Layout.Column = 3;
            app.CreatePauseBetweenFilesmsLabel.Text = 'Pause Between Files (ms)';

            % Create CreateFileCountSpinner
            app.CreateFileCountSpinner = uispinner(app.GridLayout3);
            app.CreateFileCountSpinner.Limits = [1 Inf];
            app.CreateFileCountSpinner.RoundFractionalValues = 'on';
            app.CreateFileCountSpinner.ValueDisplayFormat = '%.0f';
            app.CreateFileCountSpinner.FontSize = 16;
            app.CreateFileCountSpinner.Tooltip = {'How many files to play. For example, if the value is 5, then any 5 random files will be played.'; ''; 'The randomization is non-removed and uniform: all files have the same chance to be chosen at any time. This means that there is a chance a single file will be played File Count number of times.'};
            app.CreateFileCountSpinner.Layout.Row = 2;
            app.CreateFileCountSpinner.Layout.Column = 2;
            app.CreateFileCountSpinner.Value = 5;

            % Create CreateFileCountLabel
            app.CreateFileCountLabel = uilabel(app.GridLayout3);
            app.CreateFileCountLabel.HorizontalAlignment = 'right';
            app.CreateFileCountLabel.FontSize = 16;
            app.CreateFileCountLabel.Tooltip = {'How many files to play. For example, if the value is 5, then any 5 random files will be played.'; ''; 'The randomization is non-removed and uniform: all files have the same chance to be chosen at any time. This means that there is a chance a single file will be played File Count number of times.'};
            app.CreateFileCountLabel.Layout.Row = 2;
            app.CreateFileCountLabel.Layout.Column = 1;
            app.CreateFileCountLabel.Text = 'File Count';

            % Create CreateRandomPlaylistInfo
            app.CreateRandomPlaylistInfo = uilabel(app.GridLayout3);
            app.CreateRandomPlaylistInfo.FontSize = 18;
            app.CreateRandomPlaylistInfo.FontWeight = 'bold';
            app.CreateRandomPlaylistInfo.FontAngle = 'italic';
            app.CreateRandomPlaylistInfo.Tooltip = {'Similar to [Playback > From FIles > Audio Files > All Random (checkbox)], but this save the randomized list as a playlist .txt file instead of playing it directly.'; ''; 'Create a randomized playlist from the available audio files. Optionally, a pause in-between files can be set (aka the interstimulus interval).'; 'By creating a playlist this way, the "random" of the audio selection can be repeated if necessary later on.'};
            app.CreateRandomPlaylistInfo.Layout.Row = 1;
            app.CreateRandomPlaylistInfo.Layout.Column = 5;
            app.CreateRandomPlaylistInfo.Text = '? ';

            % Create QuicklyCreateaNewRandomPlaylistontheAudioServerLabel
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel = uilabel(app.GridLayout3);
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.HorizontalAlignment = 'center';
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.FontSize = 18;
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.FontWeight = 'bold';
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.FontColor = [0.2706 0.2706 0.2706];
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.Tooltip = {'Similar to [Playback > From FIles > Audio Files > All Random (checkbox)], but this save the randomized list as a playlist .txt file instead of playing it directly.'; ''; 'Create a randomized playlist from the available audio files. Optionally, a pause in-between files can be set (aka the interstimulus interval).'; 'By creating a playlist this way, the "random" of the audio selection can be repeated if necessary later on.'};
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.Layout.Row = 1;
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.Layout.Column = [1 4];
            app.QuicklyCreateaNewRandomPlaylistontheAudioServerLabel.Text = 'Quickly Create a New Random Playlist on the Audio Server';

            % Create CreateLamp
            app.CreateLamp = uilamp(app.GridLayout2);
            app.CreateLamp.Tooltip = {'Ready!'};
            app.CreateLamp.Layout.Row = 4;
            app.CreateLamp.Layout.Column = 2;
            app.CreateLamp.Color = [0.7412 0.851 0.6902];

            % Create InformationTab
            app.InformationTab = uitab(app.TabGroup);
            app.InformationTab.Title = 'Information';

            % Create GridLayout
            app.GridLayout = uigridlayout(app.InformationTab);
            app.GridLayout.ColumnWidth = {'1x', '1x', '5x'};
            app.GridLayout.RowHeight = {'1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x'};

            % Create InformationPanel
            app.InformationPanel = uitextarea(app.GridLayout);
            app.InformationPanel.Editable = 'off';
            app.InformationPanel.FontName = 'Cascadia Code';
            app.InformationPanel.FontSize = 11;
            app.InformationPanel.Placeholder = 'Requested information will be shown here!';
            app.InformationPanel.Layout.Row = [1 13];
            app.InformationPanel.Layout.Column = 3;

            % Create MainAPIDocumentationButton
            app.MainAPIDocumentationButton = uibutton(app.GridLayout, 'push');
            app.MainAPIDocumentationButton.ButtonPushedFcn = createCallbackFcn(app, @MainAPIDocumentationButtonPushed, true);
            app.MainAPIDocumentationButton.BackgroundColor = [0.702 0.8745 0.949];
            app.MainAPIDocumentationButton.FontSize = 14;
            app.MainAPIDocumentationButton.FontWeight = 'bold';
            app.MainAPIDocumentationButton.Layout.Row = 13;
            app.MainAPIDocumentationButton.Layout.Column = [1 2];
            app.MainAPIDocumentationButton.Text = 'Main API Documentation';

            % Create AvailableAudioFilesPlaylistsButton
            app.AvailableAudioFilesPlaylistsButton = uibutton(app.GridLayout, 'push');
            app.AvailableAudioFilesPlaylistsButton.ButtonPushedFcn = createCallbackFcn(app, @AvailableAudioFilesPlaylistsButtonPushed, true);
            app.AvailableAudioFilesPlaylistsButton.BackgroundColor = [0.949 0.902 0.6941];
            app.AvailableAudioFilesPlaylistsButton.Layout.Row = 12;
            app.AvailableAudioFilesPlaylistsButton.Layout.Column = [1 2];
            app.AvailableAudioFilesPlaylistsButton.Text = 'Available Audio Files & Playlists';

            % Create InfoDropDown
            app.InfoDropDown = uidropdown(app.GridLayout);
            app.InfoDropDown.Items = {''};
            app.InfoDropDown.ValueChangedFcn = createCallbackFcn(app, @InfoDropDownValueChanged, true);
            app.InfoDropDown.Tooltip = {'Click the buttons below to get the filtered data appears here.'};
            app.InfoDropDown.Placeholder = 'Relevant options will be shown here!';
            app.InfoDropDown.Layout.Row = 1;
            app.InfoDropDown.Layout.Column = [1 2];
            app.InfoDropDown.Value = '';

            % Create AudioFilesInfoButton
            app.AudioFilesInfoButton = uibutton(app.GridLayout, 'push');
            app.AudioFilesInfoButton.ButtonPushedFcn = createCallbackFcn(app, @AudioFilesInfoButtonPushed, true);
            app.AudioFilesInfoButton.BackgroundColor = [0.8 0.8706 0.8706];
            app.AudioFilesInfoButton.FontSize = 14;
            app.AudioFilesInfoButton.Tooltip = {'Show currently available audio files on the dropdown list.'; ''; 'If you have just Refresh the list from the Playback tab, simply click this Info button again to update.'};
            app.AudioFilesInfoButton.Layout.Row = 2;
            app.AudioFilesInfoButton.Layout.Column = 1;
            app.AudioFilesInfoButton.Text = 'Audio Files Info';

            % Create PlaylistsInfoButton
            app.PlaylistsInfoButton = uibutton(app.GridLayout, 'push');
            app.PlaylistsInfoButton.ButtonPushedFcn = createCallbackFcn(app, @PlaylistsInfoButtonPushed, true);
            app.PlaylistsInfoButton.BackgroundColor = [0.8196 0.8784 0.8196];
            app.PlaylistsInfoButton.FontSize = 14;
            app.PlaylistsInfoButton.Tooltip = {'Show currently available playlists on the dropdown list.'; ''; 'If you have just Refresh the list from the Playback tab, simply click this Info button again to update.'};
            app.PlaylistsInfoButton.Layout.Row = 2;
            app.PlaylistsInfoButton.Layout.Column = 2;
            app.PlaylistsInfoButton.Text = 'Playlists Info';

            % Create SettingsTab
            app.SettingsTab = uitab(app.TabGroup);
            app.SettingsTab.Title = 'Settings';

            % Create GridLayoutSettings
            app.GridLayoutSettings = uigridlayout(app.SettingsTab);
            app.GridLayoutSettings.ColumnWidth = {'fit', '1.2x', '0.05x', '1x', '1x'};
            app.GridLayoutSettings.RowHeight = {'1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x', '1x'};

            % Create ServerIPPortLabel
            app.ServerIPPortLabel = uilabel(app.GridLayoutSettings);
            app.ServerIPPortLabel.HorizontalAlignment = 'right';
            app.ServerIPPortLabel.FontSize = 18;
            app.ServerIPPortLabel.FontWeight = 'bold';
            app.ServerIPPortLabel.Layout.Row = 1;
            app.ServerIPPortLabel.Layout.Column = 1;
            app.ServerIPPortLabel.Text = 'Server IP : Port  ';

            % Create ServerIPPortEditField
            app.ServerIPPortEditField = uieditfield(app.GridLayoutSettings, 'text');
            app.ServerIPPortEditField.ValueChangedFcn = createCallbackFcn(app, @ServerIPPortEditFieldValueChanged, true);
            app.ServerIPPortEditField.FontSize = 22;
            app.ServerIPPortEditField.Placeholder = 'http://127.0.0.1:5055';
            app.ServerIPPortEditField.Layout.Row = 1;
            app.ServerIPPortEditField.Layout.Column = 2;
            app.ServerIPPortEditField.Value = 'http://127.0.0.1:5055';

            % Create PowerOptionsPanel
            app.PowerOptionsPanel = uipanel(app.GridLayoutSettings);
            app.PowerOptionsPanel.ForegroundColor = [0.6353 0.0784 0.1843];
            app.PowerOptionsPanel.BorderWidth = 2;
            app.PowerOptionsPanel.Title = 'Power Options';
            app.PowerOptionsPanel.BackgroundColor = [0.949 0.9098 0.9098];
            app.PowerOptionsPanel.Layout.Row = [7 11];
            app.PowerOptionsPanel.Layout.Column = [4 5];
            app.PowerOptionsPanel.FontWeight = 'bold';
            app.PowerOptionsPanel.FontSize = 16;

            % Create GridLayout6
            app.GridLayout6 = uigridlayout(app.PowerOptionsPanel);
            app.GridLayout6.ColumnWidth = {'0.85x', '1x'};
            app.GridLayout6.RowHeight = {'1x', 'fit', '1x', '0.08x', '1x'};
            app.GridLayout6.BackgroundColor = [0.949 0.9098 0.9098];

            % Create ShutdownButton
            app.ShutdownButton = uibutton(app.GridLayout6, 'push');
            app.ShutdownButton.ButtonPushedFcn = createCallbackFcn(app, @ShutdownButtonPushed, true);
            app.ShutdownButton.BackgroundColor = [0.7294 0.1176 0.1176];
            app.ShutdownButton.FontSize = 24;
            app.ShutdownButton.FontWeight = 'bold';
            app.ShutdownButton.FontColor = [0.9412 0.9412 0.9412];
            app.ShutdownButton.Tooltip = {'Shutdown the audio server. Literally, shut it down. Gone.'; ''; 'If you do not have access to the server computer, you will NOT be able to start the audio server app back up.'; ''; 'Unless you want to actually shutdown (close) the audio server app, consider using the Restart option instead.'};
            app.ShutdownButton.Layout.Row = 5;
            app.ShutdownButton.Layout.Column = 2;
            app.ShutdownButton.Text = 'Shutdown';

            % Create ShutdownServerLabel
            app.ShutdownServerLabel = uilabel(app.GridLayout6);
            app.ShutdownServerLabel.HorizontalAlignment = 'right';
            app.ShutdownServerLabel.FontSize = 18;
            app.ShutdownServerLabel.FontWeight = 'bold';
            app.ShutdownServerLabel.Tooltip = {'Shutdown the audio server. Literally, shut it down. Gone.'; ''; 'If you do not have access to the server computer, you will NOT be able to start the audio server app back up.'; ''; 'Unless you want to actually shutdown (close) the audio server app, consider using the Restart option instead.'};
            app.ShutdownServerLabel.Layout.Row = 5;
            app.ShutdownServerLabel.Layout.Column = 1;
            app.ShutdownServerLabel.Text = 'Shutdown Server  ';

            % Create ManualRestartURI
            app.ManualRestartURI = uitextarea(app.GridLayout6);
            app.ManualRestartURI.Editable = 'off';
            app.ManualRestartURI.FontName = 'Cascadia Code';
            app.ManualRestartURI.FontSize = 16;
            app.ManualRestartURI.Tooltip = {'Paste this URI into a browser URL bar, or run from the terminal with "curl" or "wget".'; ''; 'Example:'; ''; 'curl http://server_ip:port/restart?restart=true'; ''; 'wget http://server_ip:port/restart?restart=true'};
            app.ManualRestartURI.Layout.Row = 3;
            app.ManualRestartURI.Layout.Column = [1 2];

            % Create OrusetheURIbelowtoRestarttheservermanuallyLabel
            app.OrusetheURIbelowtoRestarttheservermanuallyLabel = uilabel(app.GridLayout6);
            app.OrusetheURIbelowtoRestarttheservermanuallyLabel.HorizontalAlignment = 'center';
            app.OrusetheURIbelowtoRestarttheservermanuallyLabel.VerticalAlignment = 'bottom';
            app.OrusetheURIbelowtoRestarttheservermanuallyLabel.FontSize = 18;
            app.OrusetheURIbelowtoRestarttheservermanuallyLabel.Layout.Row = 2;
            app.OrusetheURIbelowtoRestarttheservermanuallyLabel.Layout.Column = [1 2];
            app.OrusetheURIbelowtoRestarttheservermanuallyLabel.Text = 'Or use the URI below to Restart the server manually:';

            % Create RestartButton
            app.RestartButton = uibutton(app.GridLayout6, 'push');
            app.RestartButton.ButtonPushedFcn = createCallbackFcn(app, @RestartButtonPushed, true);
            app.RestartButton.BusyAction = 'cancel';
            app.RestartButton.Interruptible = 'off';
            app.RestartButton.BackgroundColor = [0.949 0.8039 0.4863];
            app.RestartButton.FontSize = 24;
            app.RestartButton.FontWeight = 'bold';
            app.RestartButton.FontColor = [0.149 0.149 0.149];
            app.RestartButton.Tooltip = {'Restart everything. From scratch.'; ''; 'Attempt to shutdown, then restart the audio server. This will stop all playing audio or process. When the server is restarted, a new log file will be use instead.'; ''; 'New playlist files created by the old process will be kept and not affected.'};
            app.RestartButton.Layout.Row = 1;
            app.RestartButton.Layout.Column = 2;
            app.RestartButton.Text = 'Restart';

            % Create RestartServerLabel
            app.RestartServerLabel = uilabel(app.GridLayout6);
            app.RestartServerLabel.HorizontalAlignment = 'right';
            app.RestartServerLabel.FontSize = 18;
            app.RestartServerLabel.FontWeight = 'bold';
            app.RestartServerLabel.Tooltip = {'Restart everything. From scratch.'; ''; 'Attempt to shutdown, then restart the audio server. This will stop all playing audio or process. When the server is restarted, a new log file will be use instead.'; ''; 'New playlist files created by the old process will be kept and not affected.'};
            app.RestartServerLabel.Layout.Row = 1;
            app.RestartServerLabel.Layout.Column = 1;
            app.RestartServerLabel.Text = 'Restart Server  ';

            % Show the figure after all components are created
            app.AudioServerClientGUIUIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = ClientGUI

            runningApp = getRunningApp(app);

            % Check for running singleton app
            if isempty(runningApp)

                % Create UIFigure and components
                createComponents(app)

                % Register the app with App Designer
                registerApp(app, app.AudioServerClientGUIUIFigure)

                % Execute the startup function
                runStartupFcn(app, @startupFcn)
            else

                % Focus the running singleton app
                figure(runningApp.AudioServerClientGUIUIFigure)

                app = runningApp;
            end

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.AudioServerClientGUIUIFigure)
        end
    end
end