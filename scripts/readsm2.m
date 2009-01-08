function out = readsm2(files); % read in one or more RHK sm2-files and convert to ascii in spectroscopy-case
% reads in RHK-.sm2-data and converts it into ascii-files (spectroscopy-data) or
% figures (image-data)
if nargin == 0
     [filenames,pathname] = uigetfile({'*.sm2'}, 'Select .sm2 Files', 'Multiselect', 'on');
     % if only one file selected create structure else sort structure
     if (class(filenames) == 'char')
         filenames = {filenames};
     else  %if (class(filenames) == 'cell')
         filenames = sort(filenames);
     end
     if (pathname == 0),
         out = -1;
         return,
     end
else
     filenames = files;
     pathname = cd;
end

% create structure array of sm2-file data
sm2 = cell(1,length(filenames));

% read in sm2-file data into structure array
for i = 1:length(filenames)
    sm2{i}.file = filenames{i};
    fh = fopen([pathname,'/',sm2{i}.file]);
    sm2{i}.file = regexprep(sm2{i}.file,'.SM2',''); % .sm2 aus dateinamen entfernen
%    mkdir(sm2{i}.file); % verzeichnis für jede datei erzeugen?
  
for j = 1:1000000
    % read header
    fields = textscan(fh, 'STiMage 3.1 %9s %9s', 1);
    sm2{i,j}.date = fields{1}{:}; sm2{i,j}.time = fields{2}{:};
    fields = textscan(fh, '%d %d %d %d %d %d %d', 1);
    [sm2{i,j}.type,sm2{i,j}.data_type,sm2{i,j}.sub_type,sm2{i,j}.x_size,sm2{i,j}.y_size,sm2{i,j}.size,sm2{i,j}.page_type] = fields{1:7};
    
    fields = textscan(fh, 'X %f %f %s', 1);
    [sm2{i,j}.xscale,sm2{i,j}.xoffset] = fields{1:2};
    sm2{i,j}.xunits = fields{3}{:};
   
% check for x.units to go ahead with import
    if (sm2{i,j}.xunits == 'Y')
        sm2{i,j}.xunits = '';
        fields = textscan(fh, '%f %f %s', 1);
    end
    if (sm2{i,j}.xunits ~= 'Y')
        fields = textscan(fh, 'Y %f %f %s', 1);
    end
    [sm2{i,j}.yscale,sm2{i,j}.yoffset] = fields{1:2};
    sm2{i,j}.yunits = fields{3}{:};

% check for y.units to go ahead with import
    if (sm2{i,j}.yunits == 'Z')
        sm2{i,j}.yunits = '';
        fields = textscan(fh, '%f %f %s', 1);
    end
    if (sm2{i,j}.yunits ~= 'Z')
        fields = textscan(fh, 'Z %f %f %s', 1);
    end
    [sm2{i,j}.zscale,sm2{i,j}.zoffset] = fields{1:2};
    sm2{i,j}.zunits = fields{3}{:};

    fields = textscan(fh, 'XY %f %*s %f', 1);
    [sm2{i,j}.xyscale,sm2{i,j}.angle] = fields{1:2};

    fields = textscan(fh, 'IV %f %f', 1);
    [sm2{i,j}.current,sm2{i,j}.bias] = fields{1:2};
    fields = textscan(fh, 'scan %d %f', 1);
    [sm2{i,j}.scan,sm2{i,j}.period] = fields{1:2}; % scan = richtung, PERIOD = S!!!
    fields = textscan(fh, 'id %d %d', 1);
    [sm2{i,j}.file_id,sm2{i,j}.data_offset] = fields{1:2};
    fields = textscan(fh, '%20c', 1);
    [sm2{i,j}.label] = fields{1};
    fields = textscan(fh, '%160s', 1);
    [sm2{i,j}.comment] = fields{1};
    
    % determine if spectroscopy or image data
 if (sm2{i,j}.type == 1)
    % check data type
      if (sm2{i,j}.data_type == 0)
    % read float-spectroscopy data
    sm2{i,j}.rawdata = fread(fh,double([sm2{i,j}.y_size,sm2{i,j}.x_size]),'float32',0,'l');
      end
      if (sm2{i,j}.data_type == 1)
    % read integer-spectroscopy data
    sm2{i,j}.rawdata = fread(fh,double([sm2{i,j}.y_size,sm2{i,j}.x_size]),'int16',0,'l');
      end
    % transpose image since matlab reads columnwise
    sm2{i,j}.rawdata = sm2{i,j}.rawdata';
 end
 if (sm2{i,j}.type == 0)
    % read image data
    sm2{i,j}.rawdata = fread(fh,double([sm2{i,j}.y_size,sm2{i,j}.x_size]),'int16',0,'l');
    % transpose image since matlab reads columnwise
    sm2{i,j}.rawdata = sm2{i,j}.rawdata';
 end

    % annotated data => spectroscopy field
 if (sm2{i,j}.type == 3)
          for (timer = 1:sm2{i,j}.y_size) % entspricht der anzahl der kurven
              % read integer-spectroscopy-field data
              sm2{i,j,timer}.rawdata = fread(fh,double([sm2{i,j}.y_size,sm2{i,j}.x_size]),'int16',0,'l'); % jede einzelne kurve
 %         end
 %         for (timer2 = 1:sm2{i,j}.y_size) % entspricht wieder der anzahl der kurven
             % fields = textscan(fh, '%f %f %f %f %f %f %f %f', 1);
             % [sm2{i,j,k}.xposition,sm2{i,j,k}.yposition] = fields{1:2};
             sm2{i,j,timer}.position = fread(fh,double([1,32]),'long',0,'l'); % anmerkung jeder einzelne kurve
          end
    % transpose image since matlab reads columnwise
    sm2{i,j,timer}.rawdata = sm2{i,j,timer}.rawdata';
 end
 
% creating labels of figures
sm2{i,j}.label = regexprep(sm2{i,j}.label,' ',''); % überflüssige leerzeichen raus
sm2{i,j}.label = regexprep(sm2{i,j}.label,'Topgraphy','Topography'); % Topgraphy -> Topography
sm2{i,j}.label = regexprep(sm2{i,j}.label,'damping','Damping'); % damping -> Damping
sm2{i,j}.label = regexprep(sm2{i,j}.label,'frequencyshift','Frequency Shift'); % frequency shift -> Frequency Shift
if (sm2{i,j}.type == 0) % nur, wenn es sich um images handelt
if (sm2{i,j}.scan == 0) % wenn es sich um 'rechts' handelt -> retrace (right)
sm2{i,j}.windowname = [sm2{i,j}.label ' - Retrace (Right)'];
end
if (sm2{i,j}.scan == 1) % wenn es sich um 'links' handelt -> trace (left)
sm2{i,j}.windowname = [sm2{i,j}.label ' - Trace (Left)'];
end
if (sm2{i,j}.scan == 2) % wenn es sich um 'up' handelt -> retrace (up)
sm2{i,j}.windowname = [sm2{i,j}.label ' - Retrace (Up)'];
end
if (sm2{i,j}.scan == 3) % wenn es sich um 'down' handelt -> trace (down)
sm2{i,j}.windowname = [sm2{i,j}.label ' - Trace (Down)'];
end
else
sm2{i,j}.windowname = [sm2{i,j}.label]; % bei spectroscopy wird das label einfach übernommen
end

% generate matrix names ----------
sm2{i,j}.matrix_name = genvarname([sm2{i}.file '_' j '_' sm2{i,j}.label]); % matlab-like name for variables
sm2{i,j}.matrix_name = regexprep(sm2{i,j}.matrix_name,'0x',''); % 0x raus
sm2{i,j}.matrix_name = regexprep(sm2{i,j}.matrix_name,'x',''); % x raus
% --------------------------------

if (sm2{i,j}.type == 0)
    % displaying properties ------------------------------------------
% set figure properties for upcoming figures
monitor=get(0,'ScreenSize'); % screensize des anwenders?
f{j} = figure(  'Position', [monitor(3) monitor(4) 600 400],... % size and position
                'DockControls','off',... % control elements werden nicht angezeigt
                'WindowStyle','docked',... % figure wird aber im figure-fenster gedocked
                'MenuBar','none',... % menü brauchen wir nicht
                'NextPlot','add',... % nächster plot überschreibt nicht den aktuellen sondern kommt hinzu
                'NumberTitle','off',... % matlab soll die figures nicht durchnumerieren
                'Name',[sm2{i,j}.windowname]); % shows actual label as windowname
f{j}; % figure wird eingelesen

% display every single page-data in command window 
disp(sm2{i,j}); 
% display every single page-data in figure 
        if (sm2{i,j}.type == 1)
           plot((1:sm2{i,j}.x_size)', sm2{i,j}.rawdata*sm2{i,j}.zscale); % spec -> figure
        end
        if (sm2{i,j}.type == 0)
           colormap summer; % farbskala für image - gray, bone, summer,...
           imagesc(sm2{i,j}.rawdata); % image -> figure
        end
% ----------------------------------------------------------------
else
% writing data to matrix-files (.txt) -------
savefile = [sm2{i}.file '.txt']; % legt den dateinamen fest, inkl. endung und verzeichnis (sm2{i}.file '\'  einfügen)
intervall = double(sm2{i,j}.x_size);
schrittweite = double(sm2{i,j}.xscale);
table{1}=['x[' sm2{i,j}.xunits ']']; % x-achsen bezeichnung
table{j+1}=[sm2{i,j}.windowname '[' sm2{i,j}.zunits ']']; % bezeichnung und einheiten der weiteren daten
savedata(:,1)=(0:schrittweite:(intervall-1)*schrittweite)'; % x-achse für alle
savedata(:,(j+1))=(sm2{i,j}.rawdata*sm2{i,j}.zscale); % jeweilige z-achsen (für spectroscopy)
% x-info schreiben, alter dateiinhalt wird gelöscht
savefilefid = fopen([sm2{i}.file '.txt'], 'wt');
fprintf(savefilefid, '%s \n', ['File: ' sm2{i}.file]);
fprintf(savefilefid, '%s \n', ['Comment: ' sm2{i,j}.comment{:}]);
fprintf(savefilefid, '%s \n', ['Date: ' sm2{i,j}.date]);
fprintf(savefilefid, '%s \n', ['Time: ' sm2{i,j}.time]);
fprintf(savefilefid, '\n');
fprintf(savefilefid, '%-8s\t', table{:});
fprintf(savefilefid, '\n');
fclose(savefilefid); % datei schliessen
% daten schreiben, inhalte werden angehängt
savefilefid = fopen([sm2{i}.file '.txt'], 'at');
lines=1;
while lines <= intervall
fprintf(savefilefid, '%-12g \t', savedata(lines,:));
fprintf(savefilefid, '\n');
lines=lines+1;
end
clear lines;
fclose(savefilefid);
% -------------------------------------------

% alles anzeigen?
%disp(table);
%disp(savedata);
%disp(sm2{i,j}); 
end
        
        
% schon am ende? ---------------------
size{i} = dir([pathname,'/',filenames{i}]); % datei-infos aus dem browser einlesen (datum, grösse, etc...)
position{i} = size{i}.bytes-ftell(fh); % position des 'cursors' in der datei

if (position{i} > 0) %cursor nicht am ende, dann weiter
    j = j+1; % liefert so die anzahl der pages insgesamt
else % cursor also am ende
    return
end

end
% end j count and close file --------
fclose(fh); % close file
end % end i count -------------------

end % end whole function ------------
