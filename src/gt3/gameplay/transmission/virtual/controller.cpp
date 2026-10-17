#include "controller.hpp"
namespace gt3::extensions::vt {
Decision Controller::step(Snapshot s,Input in){
 if(!s.maximum||s.maximum>255||s.selected>s.maximum||s.state>3)
  throw std::invalid_argument("unsupported original transmission snapshot");
 if(!attached_){accepted_=int(s.selected);attached_=true;}
 lost_|=!in.connected;
 Decision d;d.lost=lost_;
 if(lost_)accepted_=neutral; // terminal disconnect latch; no reconnection until restart
 else if(in.gear==neutral)accepted_=neutral;
 else if(in.gear<0||unsigned(in.gear)>s.maximum)d.rejected=true;
 else if(in.gear==accepted_||in.clutch||prior_clutch_||accepted_==neutral||s.state==0)
  accepted_=in.gear;
 else d.rejected=true; // reject an engaged/unclutched gear change, never invent damage
 prior_clutch_=in.clutch;
 d.gear=accepted_;d.pending=accepted_!=neutral&&unsigned(accepted_)!=s.selected;
 if(lost_||in.clutch||accepted_==neutral||d.pending)d.route=Route::free;
 else if(s.state==0)d.route=Route::synchronize;
 return d;
}
}
