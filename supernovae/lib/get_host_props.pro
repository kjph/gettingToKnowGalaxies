pro get_host_props
  ;
  ; get properties of host galaxies of SNe matched with IAU circulars
  ;
  ; G. Meurer 12/2014
  dbm       = 'supersingg_master'
  dbd       = 'singg_derived'
  film      = 'out_supernovae_match_typeII.dat'
  fmtm      = '(a,a,f,a)'
  filo      = 'supernovae_host_data.dat'
  fflist    = 'files2grab.dat'
  ;
  ; read basic supernovae data
  readcol, film, namhost, namsn, offset, type, format=fmtm
  ;
  ; open master database, and match
  dbopen, dbm
  list      = dbmatch('sname',namhost)
  ;
  ; get relevant quantities
  dbext, list, 'sname,dist,lmhi,vhel,haflag,uvflag,statoptrc,entoptphot,entfuvphot,entnuvphot', $
         sname,dist,lmhi,vhel,haflag,uvflag,statoptrc,entoptphot,entfuvphot,entnuvphot
  dbclose
  ;
  ; sort into cases of good Ha data and good UV data
  goodha       = where(entoptphot gt 0,ngoodha)
  gooduv       = where(entfuvphot gt 0 and entnuvphot gt 0, ngooduv)
  goodboth     = where(entoptphot gt 0 and entfuvphot gt 0 and entnuvphot gt 0, ngoodboth)
  goodha_baduv = where(entoptphot gt 0 and (entfuvphot le 0 or entnuvphot le 0), ngoodha_baduv)
  gooduv_badha = where((entfuvphot gt 0 and entnuvphot gt 0) and entoptphot le 0, ngooduv_badha)
  bad_both     = where(entoptphot le 0 and (entfuvphot le 0 or entnuvphot le 0), nbadboth)
  ;
  print, 'N_entries with optical photometry                           : ', ngoodha
  print, 'N_entries with UV photometry                                : ', ngooduv
  print, 'N_entries with both optical and UV photometry               : ', ngoodboth
  print, 'N_entries with optical photometry but missing UV photometry : ', ngoodha_baduv
  print, 'N_entries with UV photometry but missing optical photometry : ', ngooduv_badha
  print, 'N_entries missing both optical and UV photometry            : ', nbadboth
  ;
  ; get host galaxy optical data for the goodha cases
  ss           = sort(sname[goodha])
  goodha       = goodha[ss]
  hostnameo    = strtrim(sname[goodha],2)
  snnameo      = namsn[goodha]
  offseto      = offset[goodha]
  typeo        = type[goodha]
  ;
  disto        = dist[goodha]
  lmhio        = lmhi[goodha]
  vhelo        = vhel[goodha]
  statoptrco   = statoptrc[goodha]
  entoptphoto  = entoptphot[goodha]
  ;
  dbopen, dbd
  dbext, entoptphoto, 'name,ra,dec,axerat,pa,re_r_t,re_ha_t,rmax_f',snameo2,rao,deco,axerato,pao,rero,rehao,rmaxo
  ;
  ; get file names, put in to a big list
  flist        = make_array(2l*long(ngoodha), /string, value='')
  for ii = 0l, long(ngoodha)-1l do begin
     i0        = 2l*ii
     i1        = i0 + 1l
     ent       = entoptphoto[ii]
     fnam0     = singg_ddb_fname(ent, 'rbprofdat')
     fnam1     = singg_ddb_fname(ent, 'netbprofdat')
     flist[i0] = fnam0
     flist[i1] = fnam1
  endfor 
  dbclose
  ;
  ; get unique filenames from list
  ss           = sort(flist)
  uu           = uniq(flist[ss])
  flist        = flist[ss[uu]]
  nflist       = n_elements(uu)
  ;
  ; print results
  hdro         = '# Host       SN      Type      RA(host)   Dec(host)   a/b      PA    R_e(R) R_e(Ha)    R_max'
  fmto         = '(a28,f12.6,f12.6,f7.3,f8.2,f8.2,f8.2,f9.2)'
  openw, lo, filo, /get_lun
  ;
  printf,-1,hdro
  printf,lo,hdro
  for ii = 0, ngoodha-1 do begin
     printf,-1,ljust(hostnameo[ii],13)+ljust(snnameo[ii],8)+ljust(typeo[ii],7),rao[ii],deco[ii],axerato[ii],pao[ii],rero[ii],rehao[ii],rmaxo[ii],format=fmto
     printf,lo,ljust(hostnameo[ii],13)+ljust(snnameo[ii],8)+ljust(typeo[ii],7),rao[ii],deco[ii],axerato[ii],pao[ii],rero[ii],rehao[ii],rmaxo[ii],format=fmto
  endfor 
  free_lun, lo
  ;
  ; write list of files to grab
  openw, ll, fflist, /get_lun
  printf, -1, '# Number of profile files = '+numstr(nflist)
  printf, ll, '# Number of profile files = '+numstr(nflist)
  for ii = 0, nflist-1 do begin
     printf, -1, flist[ii], format='(a)'
     printf, ll, flist[ii], format='(a)'
  endfor 
  free_lun, ll
end


