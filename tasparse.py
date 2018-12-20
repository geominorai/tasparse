import numpy as np
import io

class Recording:
	def __init__(self, filename):
		self.filename = filename
		self.is_rec = 0
		self.is_play = 0
		self.cur_tick = 0
		self.n_ticks = 0
		self.n_pos = 0
		self.frames = []

	def str(self):
		out = io.StringIO()

		out.write('%d\n' % self.is_rec)
		out.write('%d\n' % self.is_play)
		out.write('%d\n' % self.cur_tick)
		out.write('%d\n' % self.n_ticks)
		out.write('%d\n' % self.n_pos)

		for f in self.frames:
			out.write(f.str())

		content = out.getvalue()
		out.close()
		return content

class Frame:
	def __init__(self):
		self.pos = np.empty(3, dtype=np.float32)
		self.vel = np.empty(3, dtype=np.float32)
		self.ang = np.empty(3, dtype=np.float32)
		self.butn = 0
		self.cmdnum = 0
		self.fwdmove = 0
		self.predicted = 0
		self.impulse = 0x0
		self.mouse = [0, 0]
		self.rand_seed = 0
		self.sidemove = 0
		self.tick_count = 0
		self.upmove = 0
		self.view_ang = np.empty(3, dtype=np.float32)
		self.itemdef = 0
		self.weap_subtype = 0
		self.save_frames = 0
		self.did_fire = 0
		self.clip = 0
		self.projectiles = []

	def str(self):
		out = io.StringIO()
		out.write(vec_to_str(self.pos))
		out.write(vec_to_str(self.vel))
		out.write(vec_to_str(self.ang))
		
		out.write('%d\n' % self.butn)
		out.write('%d\n' % self.cmdnum)
		out.write('%d\n' % self.fwdmove)
		
		out.write('%d\n' % self.predicted)
		if self.impulse == -1:
			out.write('\x00\n')
		else:
			out.write('%x\n' % self.impulse)
		out.write('%d\n%d\n' % (self.mouse[0], self.mouse[1]))
		out.write('%d\n' % self.rand_seed)
		out.write('%d\n' % self.sidemove)
		out.write('%d\n' % self.tick_count)
		out.write('%d\n' % self.upmove)
		out.write(vec_to_str(self.view_ang))
		
		out.write('%d\n' % self.itemdef)
		out.write('%d\n' % self.weap_subtype)

		out.write('%d\n' % self.save_frames)
		out.write('%d\n' % self.did_fire)
		out.write('%d\n' % self.clip)

		out.write('%d\n' % len(self.projectiles))
		for p in self.projectiles:
			out.write(p.str())

		content = out.getvalue()
		out.close()
		return content

class Projectile:
	def __init__(self):
		self.ang = np.empty(3, dtype=np.float32)
		self.pos = np.empty(3, dtype=np.float32)
		self.vel = np.empty(3, dtype=np.float32)
		self.type = 0

	def str(self):
		out = io.StringIO()

		out.write(vec_to_str(self.ang))
		out.write(vec_to_str(self.pos))
		out.write(vec_to_str(self.vel))
		
		out.write('%d\n' % self.type)

		content = out.getvalue()
		out.close()
		return content

def vec_to_str(vec):
	return '%s\n%s\n%s\n' % (float_to_str(vec[0]), float_to_str(vec[1]), float_to_str(vec[2]))

def float_to_str(value):
	return ('%.4f' % value).rstrip('0').rstrip('.')

def load_recording(filename):
	r = Recording(filename)

	with open(r.filename, 'rt') as file:
		r.is_rec = int(file.readline())
		r.is_play = int(file.readline())
		r.cur_tick = int(file.readline())
		r.n_ticks = int(file.readline())
		r.n_pos = int(file.readline())
		
		# print('rec=%d, play=%d, tick=%d, n_ticks=%d, n_pos=%d' % (r.is_rec, r.is_play, r.cur_tick, r.n_ticks, r.n_pos))

		# line = 5
		for i in range(r.n_ticks):
			f = Frame()
			r.frames.append(f)
			# print('Frame %d/%d: line %d' % (i+1, r.n_ticks, line+1))

			f.pos[0] = float(file.readline())
			f.pos[1] = float(file.readline())
			f.pos[2] = float(file.readline())

			f.vel[0] = float(file.readline())
			f.vel[1] = float(file.readline())
			f.vel[2] = float(file.readline())

			f.ang[0] = float(file.readline())
			f.ang[1] = float(file.readline())
			f.ang[2] = float(file.readline())

			# line += 9

			f.butn = int(file.readline())
			f.cmdnum = int(file.readline())
			f.fwdmove = int(file.readline())

			# line += 3

			# print('\tbutn=%d, cmdnum=%d, fmove=%d' % (f.butn, f.cmdnum, f.fwdmove))

			f.predicted = int(file.readline())
			impulse_raw = file.readline().strip()
			if impulse_raw == '\x00':
				f.impulse = -1
			else:
				f.impulse = int(impulse_raw, 16)
			f.mouse[0] = int(file.readline())
			f.mouse[1] = int(file.readline())
			f.rand_seed = int(file.readline())
			f.sidemove = int(file.readline())
			f.tick_count = int(file.readline())
			f.upmove = int(file.readline())
			f.view_ang[0] = float(file.readline())
			f.view_ang[1] = float(file.readline())
			f.view_ang[2] = float(file.readline())

			# line += 11

			f.itemdef = int(file.readline())
			f.weap_subtype = int(file.readline())

			# line += 2

			# print('\titemdef=%d, weap_subtype=%d' % (f.itemdef, f.weap_subtype))

			f.save_frames = int(file.readline())
			f.did_fire = int(file.readline())
			f.clip = int(file.readline())

			# line += 3

			# print('\tsave_frames=%d, did_fire=%d, clip=%d' % (f.save_frames, f.did_fire, f.clip))

			n_proj = int(file.readline())

			# line += 1

			# print('\tprojectiles=%d' % n_proj)

			for j in range(n_proj):
				p = Projectile()
				f.projectiles.append(p)

				p.ang[0] = float(file.readline())
				p.ang[1] = float(file.readline())
				p.ang[2] = float(file.readline())

				p.pos[0] = float(file.readline())
				p.pos[1] = float(file.readline())
				p.pos[2] = float(file.readline())

				p.vel[0] = float(file.readline())
				p.vel[1] = float(file.readline())
				p.vel[2] = float(file.readline())

				p.type = int(file.readline())

				# print('\t\tproj %d: ang=%s, pos=%s, vel=%s, type=%d' % (j, p.ang, p.pos, p.vel, p.type))

				# line += 10

	return r

# if __name__ == '__main__':
# 	r = load_recording('input.recording')
# 	with open('output.recording', 'wt') as file:
# 		file.write(r.str())
