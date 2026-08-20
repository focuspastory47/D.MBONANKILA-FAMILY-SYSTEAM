import 'package:flutter/material.dart';
import 'http' as http;
import 'convert';

void main() {
  runApp(const UfawakiApp());
}

class UfawakiApp extends StatelessWidget {
  const UfawakiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'UFAWAKI App',
      theme: ThemeData(
        primarySwatch: Colors.teal,
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _phoneController = TextEditingController();
  
  // **KUMBUKA:** Kama unatumia Android Emulator, tumia "http://10.0.2.2:5000"
  // Kama unajaribu kwenye simu ya mkononi kupitia Wi-Fi, weka IP ya kompyuta yako (mfano: "http://192.168.1.100:5000")
  final String baseUrl = "http://10.0.2.2:5000";

  bool _isLoading = false;
  Map<String, dynamic>? _userData;
  String? _errorMessage;

  Future<void> _fetchTaarifa() async {
    final phone = _phoneController.text.trim();
    if (phone.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Tafadhali ingiza namba ya simu!')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _userData = null;
    });

    try {
      final response = await http.get(Uri.parse('$baseUrl/api/mwanachama/$phone'));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          setState(() {
            _userData = data['mwanachama'];
          });
        } else {
          setState(() {
            _errorMessage = data['message'] ?? 'Mwanachama hajapatikana.';
          });
        }
      } else {
        setState(() {
          _errorMessage = 'Namba haijapatikana au kuna tatizo kwenye server.';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Imefeli kuunganisha na server. Hakikisha server ina-run.';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('D. MBONANKILA FAMILY (UFAWAKI)'),
        centerTitle: true,
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Card(
              elevation: 2,
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Text(
                  'Ingiza namba yako ya simu iliyosajiliwa ili kuangalia muhtasari wa malipo yako.',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 15),
                ),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _phoneController,
              keyboardType: TextInputType.phone,
              decoration: const InputDecoration(
                labelText: 'Namba ya Simu',
                hintText: 'Mfano: 255795085702',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.phone),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _fetchTaarifa,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.teal,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
              child: _isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('Angalia Taarifa', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(height: 20),
            if (_errorMessage != null) ...[
              Text(
                _errorMessage!,
                style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
            ],
            if (_userData != null) ...[
              Card(
                elevation: 4,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        _userData!['jina'] ?? '',
                        style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.teal),
                      ),
                      Text('Cheo: ${_userData!['cheo'] ?? ''}'),
                      Text('Namba: ${_userData!['namba'] ?? ''}'),
                      const Divider(height: 25, thickness: 1),
                      
                      const Text(
                        'Muhtasari wa Pesa:',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisAlignment: MainAlignment.spaceBetween,
                        children: [
                          const Text('Jumla Iliyolipwa:'),
                          Text(
                            'TSH ${_userData!['total_pesa']}',
                            style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.green),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Row(
                        mainAxisAlignment: MainAlignment.spaceBetween,
                        children: [
                          const Text('Jumla ya Faini:'),
                          Text(
                            'TSH ${_userData!['total_faini']}',
                            style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.orange),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Row(
                        mainAxisAlignment: MainAlignment.spaceBetween,
                        children: [
                          const Text('Jumla ya Deni:'),
                          Text(
                            'TSH ${_userData!['total_deni']}',
                            style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.red),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}